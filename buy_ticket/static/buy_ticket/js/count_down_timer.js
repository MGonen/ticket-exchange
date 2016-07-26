
function start_count_down_timer(time_left, event_id) {

    setInterval(function () {
         if (time_left <= 0) {
            window.location.href = '/buy-ticket/' + event_id + '/tickets/'
        }
        else {
            time_left = time_left - 1;
            time_left_minutes_and_seconds_string = convert_seconds_to_minutes_and_seconds_string(time_left);

            $('#count-down-timer').text('Time left: ' + time_left_minutes_and_seconds_string);
        }
    }, 1000);

}

function convert_seconds_to_minutes_and_seconds_string(time_left) {

    time_left_minutes = Math.floor(time_left / 60);
    time_left_seconds = time_left % 60;
    time_left_seconds_minus_2_sec = Math.max(time_left_seconds - 2, 0);
    time_left_seconds_string = ('0' + time_left_seconds_minus_2_sec.toString()).slice(-2);
    time_left_minutes_and_seconds_string = time_left_minutes + ':' + time_left_seconds_string;
    return time_left_minutes_and_seconds_string
}