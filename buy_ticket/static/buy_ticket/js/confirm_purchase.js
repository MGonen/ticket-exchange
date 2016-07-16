
function confirm_purchase_countdown(event_id) {
    var count_down_number = 60;

    setInterval(function () {
         if (count_down_number <= 0) {
            window.location.href = '/event/' + event_id + '/tickets/'
        }
        else {
            count_down_number = count_down_number - 1;
            $('#confirm_purchase_button').text('Confirm (' + count_down_number + ')');
        }
    }, 1000);

}