
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function open_login_popup(url) {
    window.open(url, "", "width=650,height=500,scrollbars=no,status=yes");
}


/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    profile_picture_opacity();
});