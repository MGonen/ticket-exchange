

// When clicking on the 'Edit' button, the form appears, the info disappears
// Furthermore, until correct data is entered and successfully ajaxed, or canceled, it is not possible to pay
function editPersonalInfo() {
    displayPersonalForm();
}

function get_data(caller) {
    var name = $("#nameInput").val();
    var email = $("#emailInput").val();

    if (caller == 'purchase') {
        return {'fullname': name, 'email': email};
    }
    else if (caller == 'sell') {
        var iban = $("#ibanInput").val();
        return {'fullname': name, 'email': email, 'iban': iban};
    }
}

function get_url(caller) {
    if (caller == 'purchase') {
        return '/buy-ticket/personal-info-ajax/'
    }

    else if (caller == 'sell') {
        return '/sell-ticket/personal-info-ajax/'
    }
}


// Ajax function call to update the changes entered in the form
function savePersonalInfo(caller) {

    data = get_data(caller);
    url = get_url(caller);

    hideFormErrorMessage();
    // console.log(data);

    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: data,
        url: url,
        success: function (results) {
            updatePersonalInfo(results['new_name'], results['new_email'], results['new_iban']);
            displayPersonalInfo();
        },
        error: function (results) {
            var errors = (JSON.parse(results.responseText)['errors']);
            updateErrorMessage(errors.join(', '));
            showFormErrorMessage();
        }
    });
}

function updatePersonalInfo(fullname, email, iban) {
    $("#nameStatic").text(fullname);
    $("#emailStatic").text(email);
    $("#ibanStatic").text(iban);
}

function createFormErrorMessage() {
    var error_message_element = document.createElement('p');
    error_message_element.id = "errorMessageElement";
    $("#personalInfoButtons").prepend(error_message_element);
    $("#errorMessageElement").hide()
}

function updateErrorMessage(errors) {
    var errorMessage = 'The following field(s) are incorrect: ' + errors;
    console.log(errorMessage);
    $("#errorMessageElement").text(errorMessage);
}

function showFormErrorMessage(){
    $("#errorMessageElement").show()
}

function hideFormErrorMessage(){
    $("#errorMessageElement").hide()
}

function cancelPersonalInfoChange() {
    // re-insert original name and email as value in form-fields
    name_static = $("#nameStatic").text();
    $("#nameInput").val(name_static);
    email_static = $("#emailStatic").text();
    $("#emailInput").val(email_static);
    iban_static = $("#ibanStatic").text();
    $("#ibanInput").val(iban_static);

    displayPersonalInfo();
    hideFormErrorMessage();
}

function displayPersonalForm() {
    $("#nameStatic").hide();
    $("#emailStatic").hide();
    $("#ibanStatic").hide();
    $("#nameInput").show();
    $("#emailInput").show();
    $("#ibanInput").show();

    $("#editPersonalInfo").hide();
    $("#savePersonalInfo").show();
    $("#cancelPersonalInfo").show();

    $("#purchaseButton").hide();
}

function displayPersonalInfo(){
    $("#nameInput").hide();
    $("#emailInput").hide();
    $("#ibanInput").hide();
    $("#nameStatic").show();
    $("#emailStatic").show();
    $("#ibanStatic").show();

    $("#savePersonalInfo").hide();
    $("#cancelPersonalInfo").hide();
    $("#editPersonalInfo").show();

    $("#purchaseButton").show();
}


$(document).ready( function() {
    displayPersonalInfo();
    createFormErrorMessage();
});

