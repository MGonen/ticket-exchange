
function start_get_event_tickets_js(event_id){

    ajax_event_tickets_call(event_id);
    setInterval(function() {
        ajax_event_tickets_call(event_id)
    }, 5000);
}

function ajax_event_tickets_call(event_id) {
    url = '/get_event_tickets/' + event_id + '/';

    $.ajax({
        url: url,
        type: "GET",
        cache: false,
        success: function(results) {
            $('.list-group').remove();
            $('.event_ticket_form_content').remove();
            if (results.already_a_potential_buyer){
                create_form_content();
            }
            else {
                ticket_removed_message();
                var ticket_list = create_event_ticket_list(results.tickets);
                $('.continue_ticket_purchase_form').after(ticket_list);
            }

        },
        error: function () {
            console.log('js error')
        }
    });
}

function create_form_content() {
    var info_text_element = document.createElement('p');
    info_text_element.className = 'event_ticket_form_content';
    info_text_element.innerText = 'You are already in the process of buying a ticket. Would you like to continue, or select a different ticket';


    var continue_button = document.createElement('button');
    continue_button.name = 'continue';
    continue_button.className = 'btn btn-primary event_ticket_form_content';
    continue_button.innerText = 'Continue with selected ticket';

    var different_ticket_button = document.createElement('button');
    different_ticket_button.name = 'new';
    different_ticket_button.className = 'btn btn-primary event_ticket_form_content';
    different_ticket_button.innerText = 'Select a different ticket';

    $('.continue_ticket_purchase_form').append(info_text_element);
    $('.continue_ticket_purchase_form').append(continue_button);
    $('.continue_ticket_purchase_form').append(different_ticket_button);

}


function ticket_removed_message() {
    var message = document.createElement('div');
    message.innerText = "If you were in the process of buying a ticket and it's gone, it means you you took too long to buy the ticket. Please select a ticket again, and this time try to be a bit quicker ;-)";
    message.className = "alert alert-info";
    message.id = 'ticket_removed_message';

    $('#ticket_removed_message').remove();
    $('.messagelist').append(message);
}


function create_event_ticket_list(tickets) {
    var ticket_list = document.createElement('div');
    ticket_list.className = 'list-group';

    ticket_list = append_event_ticket_items(ticket_list, tickets);

    return ticket_list
}


function append_event_ticket_items(ticket_list, tickets) {

    for (var i=0; i < tickets.length; i++ ) {
        var ticket_item = create_event_ticket_item(tickets[i]);

        ticket_list.appendChild(ticket_item);
    }

    return ticket_list

}

function create_event_ticket_item(ticket){

    var ticket_item = document.createElement('a');

    var ticket_link = "/buy-ticket/potential_buyer_check/" + ticket.id + '/';
    ticket_item.setAttribute('href', ticket_link);
    ticket_item.className = 'list-group-item';

    var ticket_item_heading = document.createElement('h4');
    ticket_item_heading.className = 'list-group-item-heading';
    ticket_item_heading.innerHTML = '&euro; ' + ticket.price;
    ticket_item_heading.style.color = '#0081db';

    var ticket_item_text = document.createElement('p');
    ticket_item_text.className = 'list-group-item-text';
    ticket_item_text.innerText = ticket.seller;
    ticket_item.appendChild(ticket_item_heading);
    ticket_item.appendChild(ticket_item_text);

    return ticket_item
}



function reload_page() {
    console.log('arrived at reload page');
    location.reload()
}


/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    // ajax_event_tickets_call();
    // reload_page();
});