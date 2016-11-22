


function parsley_price_general() {
    $price_input = $('#id_price');
    $price_input.attr('placeholder',"\u20AC12.34");

    $price_input.attr('data-parsley-required',"true");
    $price_input.attr('min', 0);

    const parsley_price_pattern = "^([0-9]*\.[0-9]{2})$";
    $price_input.attr('data-parsley-pattern', parsley_price_pattern);
    $price_input.attr('data-parsley-pattern-message',"Must be a number with 2 decimal places");
}

function parsley_price_max() {
    $price_input.attr('max', max_ticket_price);
}

function parsley_pdf_file() {
    $pdf_file_upload = $('#id_pdf_file');
    $pdf_file_upload.attr('data-parsley-required',"true");
}


$(document).ready( function() {
    parsley_price_general();
    parsley_price_max();
    parsley_pdf_file()
});