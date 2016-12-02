from django.core.files import File
import scriptine

from ticket_exchange.pdfs import ProcessTicket, ProcessBaseTicket


pdf_filepath = scriptine.path('/home/michael/Documents/Ticket Exchange/ticket pdfs/eTicket.pdf')
pdf = File(open(pdf_filepath))

pdf_object = ProcessBaseTicket(pdf)