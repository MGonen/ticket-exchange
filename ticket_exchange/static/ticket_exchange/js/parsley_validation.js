// Ticket Validation

function parsley_price_general() {
    $price_input = $('#id_price');
    $price_input.attr('placeholder',"\u20AC12.34");

    $price_input.attr('data-parsley-required',"true");
    $price_input.attr('min', 0);

    const parsley_price_pattern = "[0-9]+\\.[0-9][0-9]";
    $price_input.attr('data-parsley-pattern', parsley_price_pattern);
    $price_input.attr('data-parsley-pattern-message',"Must be a number with 2 decimal places");
}


function parsley_pdf_file_required() {
    $pdf_file_upload = $('#id_pdf_file');
    $pdf_file_upload.attr('data-parsley-required',"true");
}

