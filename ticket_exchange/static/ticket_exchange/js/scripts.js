
$(function() {

    $(".date_form_input").datepicker ({
        startDate: '-1d',
        format: "dd-mm-yyyy"
        });
});


function profile_picture_opacity() {
    $('.image-button').hover(function() {
        $(this).find('.facebook-image').css('opacity', '0.8');
    }, function() {
        $(this).find('.facebook-image').css('opacity', '0.6');
    });
}


function open_login_popup(url) {
    window.open(url, "", "width=650,height=500,scrollbars=no,status=yes");
}


/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    profile_picture_opacity();
});