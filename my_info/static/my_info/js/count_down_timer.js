function remove_ticket_count_down_timer() {
    var time_left = 15;
    setInterval(function () {
         if (time_left <= 0) {
             window.location.replace(cancel_remove_url);
        }
        else {
            time_left = time_left - 1;
            $('#submit').text('Remove (' + time_left + ')');
        }
    }, 1000);

}

$(document).ready( function() {
    remove_ticket_count_down_timer();
});