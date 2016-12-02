from django.conf import settings

from wand.image import Image as WandImage
import zbar
from PIL import Image as PILImage
import scriptine
import datetime
from collections import namedtuple

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

        # Some other checks.

        self.successful = True
        return


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
        # If there are no barcodes, the pdf is invalid
        if not self.barcode_objects:
            self.message = messages.pdf_invalid
            return False

        # If the number of barcodes in the baseticket and this ticket is not equal, the pdf is invalid
        # if len(barcode_dicts) != len(Barcode.objects.filter(baseticket_event_id=self.event_id)):
        #     self.message = messages.pdf_invalid
        #     return False

        # for barcode_dict in barcode_dicts:
        #     barcode_dictsbase_ticket_barcodes
        #     base_ticket_barcode_types = ticket.
        #     if not barcode.type == BaseTicket.objects.get(event_id=self.event_id).type

            # barcodes = { ticket.barcode for ticket in Ticket.objects.filter(event_id=self.event_id) }
            # if barcode_dict['number'] in barcodes:
            #     self.message = messages.pdf_already_uploaded
            #     return False

        return True


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
        for barcode_object in pdf_object.barcode_objects:
            type = BaseTicketBarcodeType(baseticket_id=baseticket_id, type=barcode_object.type)
            type.save()
            for bc_location in barcode_object.locations:
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
