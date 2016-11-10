
function start_count_down_timer(time_left, event_id) {

    setInterval(function () {
         if (time_left <= 0) {
             window.location.replace('/buy-ticket/' + event_id + '/tickets/');
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

function setupBraintreeAjax() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/buy-ticket/payment/token/',
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

// When clicking on the 'Edit' button, the form appears, the info disappears
// Furthermore, until correct data is entered and successfully ajaxed, or canceled, it is not possible to pay
function editPersonalInfo() {
    displayPersonalForm();
}

// Ajax function call to update the changes entered in the form
function savePersonalInfo() {
    var name = $("#inputName").val();
    var email = $("#inputEmail").val();

    data = {'fullname': name, 'email': email};
    hideFormErrorMessage();

    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: data,
        url: '/buy-ticket/personal-info-ajax/',
        success: function (results) {
            updatePersonalInfo(results['new_name'], results['new_email']);
            displayPersonalInfo();
        },
        error: function () {
            showFormErrorMessage();
        }
    });
}

function updatePersonalInfo(fullname, email) {
    $("#nameInfo").text(fullname);
    $("#emailInfo").text(email);
}

function createFormErrorMessage() {
    var error_message_element = document.createElement('p');
    error_message_element.id = "errorMessageElement";
    error_message_element.innerText = 'Make sure you enter a valid name and email address in these fields';
    $("#purchase-personal-details-form").append(error_message_element);
    $("#errorMessageElement").hide()
}

function showFormErrorMessage(){
    $("#errorMessageElement").show()
}

function hideFormErrorMessage(){
    $("#errorMessageElement").hide()
}

function cancelPersonalInfoChange() {
    // re-insert original name and email as value in form-fields
    name_info = $("#nameInfo").text();
    $("#inputName").val(name_info);
    email_info = $("#emailInfo").text();
    $("#inputEmail").val(email_info);

    displayPersonalInfo();
}

function displayPersonalForm() {
    $("#purchase-personal-details-form").show();
    $("#purchase-personal-details-info").hide();
    $("#purchaseButton").hide();
}

function displayPersonalInfo(){
    $("#purchase-personal-details-info").show();
    $("#purchase-personal-details-form").hide();
    $("#purchaseButton").show();
}


$(document).ready( function() {
    displayPersonalInfo();
    createFormErrorMessage();
});

