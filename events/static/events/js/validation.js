
// Event validation
function parsley_event_general() {
    $location_input = $('#id_location');
    $city_input = $('#id_city');
    $country_input = $('#id_country');
    $start_date = $('#id_start_date');
    $end_date = $('#id_end_date');

    $location_input.attr('data-parsley-required',"true");
    $city_input.attr('data-parsley-required',"true");
    $country_input.attr('data-parsley-required',"true");
    $start_date.attr('data-parsley-required',"true");
    $end_date.attr('data-parsley-required',"true");

}

function parsley_event_name() {
    $name_input = $('#id_name');
    $name_input.attr('data-parsley-required',"true");
    $name_input.attr('data-parsley-two_characters',"true");

    window.Parsley.addValidator('two_characters', {
        validateString: function(value) {
            value = value.replace(' ', '');
            return value.length >= 2;
        },
        messages: {
            en: 'Event name must be at least two characters'
        }
    });

}


function parsley_event_dates() {
    $start_date = $('#id_start_date');
    $end_date = $('#id_end_date');
    $start_date.attr('data-parsley-dates',"true");

    window.Parsley.addValidator('dates', {
        validateString: function(value) {
            return $end_date.val() >= $start_date.val()
        },
        messages: {
            en: 'The end date must be on the same or later date than the start date'
        }
    });
}


$(document).ready( function() {
    parsley_event_general();
    parsley_event_name();
    parsley_price_general();
    parsley_event_dates();

    if (!pdf_exists) {parsley_pdf_file_required()}
});