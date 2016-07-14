

function show_commissioned_price() {
    $('#price_form_input').keyup(function() {
        input_price = $('#price_form_input').val();
        var returned_price = (input_price * 0.92) - .3;
        returned_price = returned_price.toFixed(2);
        $('#price_after_commission').text(returned_price);
    })
}


$(document).ready( function() {
    show_commissioned_price();
});
