from django.conf import settings

from wand.image import Image as WandImage
import zbar
from PIL import Image as PILImage
import scriptine
import datetime
from collections import namedtuple

from reportlab.lib.pagesizes import A4
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
import random

from ticket_exchange.models import Ticket, Event, BaseTicket, BaseTicketBarcodeType, BaseTicketBarcodeLocation, TicketBarcodeNumber
from ticket_exchange import messages


class ProcessPdf(object):

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.file_path = None
        self.successful = False
        self.barcode_objects = None
        self.message = 'Unspecified error'

    def pdf_is_safe(self):
        # return virus_scanner(self.pdf)
        return True

    def get_this_ticket_barcode_types(self):
        types = []
        for barcode in self.barcode_objects:
            types.append(str(barcode.type))

        return types

    def get_this_ticket_barcode_locations(self):
        locations = []
        for barcode in self.barcode_objects:
            locations += barcode.locations

        return locations

    def get_this_ticket_barcode_numbers(self):
        this_ticket_barcodes = set()

        for barcode in self.barcode_objects:
            this_ticket_barcodes.add(barcode.number)

        return this_ticket_barcodes


class ProcessBaseTicket(ProcessPdf):

    def __init__(self, pdf_file):
        super(ProcessBaseTicket, self).__init__(pdf_file)
        self.pdf_file = pdf_file
        self.main()


    def main(self):
        if not self.pdf_is_safe():
            self.message = messages.unsafe_pdf
            return

        self.barcode_objects = GetBarcodesPDF.extract(self.pdf_file)
        if not self.barcode_objects:
            return

        if not self.pdf_is_valid:
            return

        # Perhaps 2 different tickets need to be uploaded to make sure there are no mistakes?

        self.successful = True
        return

    def pdf_is_valid(self):
        """BaseTicket must have at least 1 type, 1, location and 1 number"""
        self.message = messages.pdf_invalid

        if not self.get_this_ticket_barcode_types():
            return False

        if not self.get_this_ticket_barcode_locations():
            return False

        if not self.get_this_ticket_barcode_numbers():
            return False

        return True


class ProcessTicket(ProcessPdf):

    def __init__(self, pdf_file, event_id):
        super(ProcessTicket, self).__init__(pdf_file)
        self.pdf_file = pdf_file
        self.event_id = event_id
        self.main()

    def main(self):
        if not self.pdf_is_safe():
            self.message = messages.unsafe_pdf
            return

        self.barcode_objects = GetBarcodesPDF.extract(self.pdf_file)
        if not self.pdf_is_valid():
            return


        self.successful = True
        return


    def pdf_is_valid(self):
        self.message = messages.pdf_invalid
        # If there are no barcodes, the pdf is invalid
        if not self.barcode_objects:
            return False

        baseticket_id = BaseTicket.objects.get(event_id=self.event_id).id
        if not self.barcode_types_are_valid(baseticket_id):
            print 'types invalid'
            return False

        if not self.barcode_locations_are_valid(baseticket_id):
            print 'locations invalid'
            return False

        if not self.barcode_numbers_are_valid():
            self.message = messages.pdf_already_uploaded
            print 'numbers invalid'
            return False

        self.message = ''
        return True


    def barcode_types_are_valid(self, baseticket_id):
        """
        This function checks whether both baseticket and this ticket have types
        Whether baseticket and this ticket have the same number of types
        Whether the set of the baseticket types and set of types of this ticket is equal
        """
        base_ticket_types = [ item.type for item in BaseTicketBarcodeType.objects.filter(baseticket_id=baseticket_id) ]
        this_ticket_types = self.get_this_ticket_barcode_types()

        if not base_ticket_types or not this_ticket_types:
            print 'types not present'
            return False

        if len(base_ticket_types) != len(this_ticket_types):
            print 'number of types not equal'
            return False

        if set(base_ticket_types) != set(this_ticket_types):
            print 'type sets not equal'
            return False

        return True


    def barcode_locations_are_valid(self, baseticket_id):
        """
        This function checks whether both baseticket and this ticket have locations
        Whether baseticket and this ticket have the same number of locations
        Whether each location of this ticket is in the same location (+- 20px) as the locations of the baseticket
        """
        base_ticket_locations = BaseTicketBarcodeLocation.objects.filter(baseticket_id=baseticket_id)
        this_ticket_locations = self.get_this_ticket_barcode_locations()

        if not base_ticket_locations or not this_ticket_locations:
            print 'locations missing'
            return False

        if len(base_ticket_locations) != len(this_ticket_locations):
            print len(base_ticket_locations), len(this_ticket_locations)
            print 'number of locations not equal'
            return False

        for location in this_ticket_locations:
            if not self.barcode_location_in_baseticket_barcode_locations(location, base_ticket_locations):
                print 'location not present in baseticket'
                return False

        return True


    def barcode_location_in_baseticket_barcode_locations(self, location, base_ticket_locations):
        for base_ticket_location in base_ticket_locations:
            x_min_equal = abs(location.x_min - base_ticket_location.x_min) <= 20
            x_max_equal = abs(location.x_max - base_ticket_location.x_max) <= 20
            y_min_equal = abs(location.y_min - base_ticket_location.y_min) <= 20
            y_max_equal = abs(location.y_max - base_ticket_location.y_max) <= 20

            if x_min_equal and x_max_equal and y_min_equal and y_max_equal:
                return True

        return False


    def barcode_numbers_are_valid(self):
        """
        Checks whether the barcodes in the ticket are unique.
        One barcode can correspond to another in the list, as long as the set of barcodes per ticket is unique
        """
        this_ticket_barcodes = self.get_this_ticket_barcode_numbers()
        existing_ticket_barcodes = self.get_existing_ticket_barcode_numbers()

        if this_ticket_barcodes in existing_ticket_barcodes:
            return False

        return True


    def get_existing_ticket_barcode_numbers(self):
        tickets = Ticket.objects.filter(event_id=self.event_id)
        existing_ticket_barcodes = []

        for ticket in tickets:
            barcodes_per_ticket = {barcode.number for barcode in ticket.ticketbarcodenumber_set.all()}
            existing_ticket_barcodes.append(barcodes_per_ticket)

        return existing_ticket_barcodes



class GetBarcodesPDF():
    BarcodeNT = namedtuple('BarcodeNT', ['type', 'number', 'locations'])

    @classmethod
    def extract(cls, pdf_file):
        filename = SavePDF.get_now_in_string()

        pdf_filepath = SavePDF.create_ticket_filepath(SavePDF.TEMPORARY_PDF_FOLDER, filename)
        SavePDF.save_pdf(pdf_file, pdf_filepath)

        image_filepath = SavePDF.create_ticket_filepath(SavePDF.TEMPORARY_PNG_FOLDER, filename, extension='.png')
        cls._convert_pdf_to_png_and_save(pdf_filepath, image_filepath)

        barcode_objects = cls._extract_barcodes_from_png(image_filepath)
        return barcode_objects

    @classmethod
    def _convert_pdf_to_png_and_save(cls, pdf_filepath, image_filepath):
        with WandImage(filename=pdf_filepath, resolution=300) as img:
            img.alpha_channel = False
            img.save(filename=image_filepath)

    @classmethod
    def _extract_barcodes_from_png(cls, image_filepath):
        pil = PILImage.open(image_filepath).convert('L')

        scanner = zbar.ImageScanner()
        image = zbar.Image(pil.width, pil.height, 'Y800', pil.tobytes())
        scanner.scan(image)

        barcode_objects = []
        for symbol in image:
            barcode_object = cls.BarcodeNT(type=symbol.type, number=symbol.data, locations=BarcodeLocation.get_outer_values(symbol.location))
            barcode_objects.append(barcode_object)

        return barcode_objects


class BarcodeLocation():
    LocationNT = namedtuple('LocationNT', ['x_min', 'x_max', 'y_min', 'y_max'])

    def __init__(self, tuples):
        self.tuples = tuples
        self.outer_values_list = []
        self.extract_outer_values()

    @classmethod
    def get_outer_values(self, tuples):
        instance = BarcodeLocation(tuples)
        return instance.outer_values_list

    def extract_outer_values(self):
        vertical_sequences = self.sequence_search(0)
        horizontal_sequences = self.sequence_search(1)

        vertical_sequences = [x for x in vertical_sequences if x]
        horizontal_sequences = [x for x in horizontal_sequences if x]

        for sequence in horizontal_sequences:
            self.outer_values_list.append(self.get_horizontal_sequence_outer_values(sequence))


        for sequence in vertical_sequences:
            self.outer_values_list.append(self.get_horizontal_sequence_outer_values(sequence))

    def sequence_search(self, value):
        sequences = []
        new_sequence = []
        for item_number in range(len(self.tuples) - 1):
            if 0 <= self.tuples[item_number + 1][value] - self.tuples[item_number][value] <= 1:
                new_sequence.append(self.tuples[item_number])
            else:
                if new_sequence:
                    sequences.append(new_sequence)
                new_sequence = []
        sequences.append(new_sequence)

        return sequences

    def get_horizontal_sequence_outer_values(self, sequence):
        y_min = sequence[0][1]
        y_max = sequence[-1][1]
        x_values = {item[0] for item in sequence}
        x_min = min(x_values)
        x_max = max(x_values)

        return self.LocationNT(x_min = x_min, x_max = x_max, y_min=y_min, y_max=y_max)

    def get_vertical_sequence_outer_values(self, sequence):
        x_min = sequence[0][0]
        x_max = sequence[-1][0]
        x_values = {item[1] for item in sequence}
        y_min = min(x_values)
        y_max = max(x_values)

        return self.LocationNT(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)


class SavePDF():
    BASE_TICKET_FOLDER = 'base_tickets'
    FESTIVAL_TICKET_FOLDER = 'festival_tickets'
    TEMPORARY_PDF_FOLDER = 'temporary_pdfs'
    TEMPORARY_PNG_FOLDER = 'temporary_pngs'

    @classmethod
    def save_festival_ticket_return_filepath(cls, pdf_object, ticket_id):
        cls.save_festival_barcode_number(pdf_object, ticket_id)
        filename = str(ticket_id)
        filepath = cls.create_ticket_filepath(cls.FESTIVAL_TICKET_FOLDER, filename)
        cls.save_pdf(pdf_object.pdf_file, filepath)
        return filepath

    @classmethod
    def save_festival_barcode_number(cls, pdf_object, ticket_id):
        for barcode_objects in pdf_object.barcode_objects:
            # Save Barcode number for this barcode in Ticket
            number = TicketBarcodeNumber(ticket_id=ticket_id, number=barcode_objects.number)
            number.save()

    @classmethod
    def save_base_ticket_return_filepath(cls, pdf_object, event_id):
        cls.save_base_barcode_info(pdf_object, event_id)
        filename = str(event_id)
        filepath = cls.create_ticket_filepath(cls.BASE_TICKET_FOLDER, filename)
        cls.save_pdf(pdf_object.pdf_file, filepath)
        return filepath

    @classmethod
    def save_base_barcode_info(cls, pdf_object, event_id):
        baseticket_id = BaseTicket.objects.get(event_id=event_id).id

        BaseTicketBarcodeType.objects.filter(baseticket_id=baseticket_id).delete()
        BaseTicketBarcodeLocation.objects.filter(baseticket_id=baseticket_id).delete()

        for barcode_object in pdf_object.barcode_objects:
            # Save the barcode type for this Barcode in BaseTicket
            type = BaseTicketBarcodeType(baseticket_id=baseticket_id, type=barcode_object.type)
            type.save()

            for bc_location in barcode_object.locations:
                # Save the barcode locations
                barcode_location_db_object = BaseTicketBarcodeLocation(baseticket_id=baseticket_id, x_min= bc_location.x_min, x_max=bc_location.x_max, y_min=bc_location.y_min, y_max=bc_location.y_max)
                barcode_location_db_object.save()

    @classmethod
    def get_now_in_string(self):
        now = datetime.datetime.now()
        return "%i%02i%02i:%02i%02i%02i" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    @classmethod
    def create_ticket_filepath(cls, folder_name, extensionless_filename, extension='.pdf'):
        tickets_directory = scriptine.path(settings.STATIC_ROOT).joinpath('tickets')
        if not tickets_directory.exists():
            tickets_directory.mkdir()

        specific_tickets_directory = tickets_directory.joinpath(folder_name)
        if not specific_tickets_directory.exists():
            specific_tickets_directory.mkdir()

        filepath = specific_tickets_directory.joinpath(extensionless_filename)
        filepath += extension
        return filepath


    @classmethod
    def save_pdf(cls, pdf_file, filepath):
        with open(filepath, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)


def create_test_baseticket_pdf(response, barcode_value):
    x_location = random.randrange(10, 500)
    y_location = random.randrange(20, 700)

    return create_ticket_pdf(response, barcode_value, x_location, y_location, 'Test BaseTicket')

def create_test_event_ticket_pdf(response, barcode_value, event):
    # Get X and Y Locations to make a ticket identical to the base ticket
    baseticket_x_location = event.baseticket.baseticketbarcodelocation_set.all()[0].x_min
    x_location = (baseticket_x_location - 34) / 4.17

    baseticket_y_location = event.baseticket.baseticketbarcodelocation_set.all()[0].y_min
    y_location = (3202 - baseticket_y_location) / 4.17

    return create_ticket_pdf(response, barcode_value, x_location, y_location, event.name)

def create_ticket_pdf(response, barcode_value, x_location, y_location, title):
    # Create the PDF object, using the response object as its "file."
    c = canvas.Canvas(response, pagesize=A4)

    # Create the barcode, using the supplied barcode value
    barcode_eanbc8 = eanbc.Ean8BarcodeWidget(barcode_value)

    # Draw things on the PDF. Here's where the PDF generation happens.
    d = Drawing(50, 10)
    d.add(barcode_eanbc8)
    renderPDF.draw(d, c, x_location, y_location)

    c.drawString(200, 800, "%s - %s" % (title, barcode_value))

    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()

    return response