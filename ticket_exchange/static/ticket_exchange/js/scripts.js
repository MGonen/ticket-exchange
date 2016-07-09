
$(function() {

    $(".date").datepicker ({
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





/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    profile_picture_opacity();
});