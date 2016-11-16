function remove_ticket_count_down_timer(ticket_id) {

    var time_left = 15;
    setInterval(function () {
         if (time_left <= 0) {
             window.location.replace('/my-info/tickets/for-sale/' + ticket_id + '/cancel-remove/');
        }
        else {
            time_left = time_left - 1;
            $('#submit').text('Remove (' + time_left + ')');
        }
    }, 1000);

}
