

// When clicking on the 'Edit' button, the form appears, the info disappears
// Furthermore, until correct data is entered and successfully ajaxed, or canceled, it is not possible to pay
function editPersonalInfo() {
    event.preventDefault();
    displayPersonalForm();
}

function savePersonalInfo(caller) {
    event.preventDefault();
    $form = $('#personalInfoForm');
    $form.parsley().validate();
    if ($form.parsley().isValid()) {
        savePersonalInfoAjax(caller)
    }
}

function cancelPersonalInfoChange() {
    event.preventDefault();
    $form = $('#personalInfoForm');
    $form.parsley().reset();
    reset_values()
}

function get_data() {
    var name = $("#nameInput").val();
    var email = $("#emailInput").val();
    var iban = $("#ibanInput").val();

    return {'fullname': name, 'email': email, 'iban': iban};
}

// Ajax function call to update the changes entered in the form
function savePersonalInfoAjax() {

    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: get_data(),
        url: '/my-info/profile/ajax/',
        success: function (results) {
            updatePersonalInfo(results['new_name'], results['new_email'], results['new_iban']);
            displayPersonalInfo();
        },
        error: function () {
            console.log('js errors')
        }
    });
}

function updatePersonalInfo(fullname, email, iban) {
    $("#nameStatic").text(fullname);
    $("#emailStatic").text(email);
    $("#ibanStatic").text(iban);
}

function reset_values() {
    // re-insert original name and email as value in form-fields
    name_static = $("#nameStatic").text();
    $("#nameInput").val(name_static);
    email_static = $("#emailStatic").text();
    $("#emailInput").val(email_static);
    iban_static = $("#ibanStatic").text();
    $("#ibanInput").val(iban_static);

    displayPersonalInfo();
}

function displayPersonalForm() {
    $("#nameStatic").hide();
    $("#emailStatic").hide();
    $("#ibanStatic").hide();
    $("#nameInput").show();
    $("#emailInput").show();
    $("#ibanInput").show();

    $("#editPersonalInfoButton").hide();
    $("#savePersonalInfoButton").show();
    $("#cancelPersonalInfoChangeButton").show();

    $("#purchaseButton").hide();
}

function displayPersonalInfo(){
    $("#nameInput").hide();
    $("#emailInput").hide();
    $("#ibanInput").hide();
    $("#nameStatic").show();
    $("#emailStatic").show();
    $("#ibanStatic").show();

    $("#savePersonalInfoButton").hide();
    $("#cancelPersonalInfoChangeButton").hide();
    $("#editPersonalInfoButton").show();

    $("#purchaseButton").show();
}


$(document).ready( function() {
    displayPersonalInfo();
});

