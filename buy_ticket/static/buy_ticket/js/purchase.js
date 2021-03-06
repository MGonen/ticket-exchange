

function ajax_count_down_timer() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        cache: false,
        url: purchase_time_left_url,
        success: function (results) {
            start_count_down_timer(results.time_left);
        },
        error: function () {
            console.log('js error')
        }
    });
}

function start_count_down_timer(time_left) {
    setInterval(function () {
         if (time_left <= 0) {
             window.location.replace(available_tickets_url);
        }
        else {
             if (time_left <= 1) {$('#purchaseButton').hide()}

             time_left = time_left - 1;
             time_left_minutes_and_seconds_string = convert_seconds_to_minutes_and_seconds_string(time_left);
             $('#count-down-timer').text('Time left: ' + time_left_minutes_and_seconds_string);
        }
    }, 1000);

}

function convert_seconds_to_minutes_and_seconds_string(time_left) {

    time_left_minutes = Math.floor(time_left / 60);
    time_left_seconds = time_left % 60;
    time_left_seconds_string = ('0' + time_left_seconds.toString()).slice(-2);
    time_left_minutes_and_seconds_string = time_left_minutes + ':' + time_left_seconds_string;
    return time_left_minutes_and_seconds_string
}

function setupBraintreeAjax() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: get_token_url,
        success: function (results) {
            braintree.setup(results.token, 'dropin', {
                container: 'dropin-container'
            })
        },
        error: function () {
            console.log('js error')
        }
    });
}

$(document).ready( function() {
    ajax_count_down_timer();
});