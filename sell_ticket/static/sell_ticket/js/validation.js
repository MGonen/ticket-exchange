

function parsley_price_max() {
    $price_input.attr('max', max_ticket_price);
}

$(document).ready( function() {
    parsley_price_general();
    parsley_price_max();
    parsley_pdf_file_required()
});