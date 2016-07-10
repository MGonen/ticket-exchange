
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


function logging_in() {
    $('#login-button').click(function () {
        document.getElementById("login-button").innerText = "Logging in...";
        document.getElementById("login-button").className = "logging-in";
        document.getElementById("login-button").style.color = "white";
    })
}



/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    profile_picture_opacity();
    logging_in();
});