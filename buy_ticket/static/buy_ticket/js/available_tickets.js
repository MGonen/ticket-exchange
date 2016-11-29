
function start_get_available_tickets_js(){

    ajax_available_tickets_call();
    setInterval(function() {
        ajax_available_tickets_call()
    }, 5000);
}

function ajax_available_tickets_call() {
    $.ajax({
        url: get_available_tickets_url,
        type: "GET",
        cache: false,
        success: function(results) {
            $('.list-group').remove();
            $('#already_buying').remove();
            if (results.already_a_potential_buyer){
                create_form_content(results.selected_ticket);
            }
            else {
                // ticket_removed_message();
                var ticket_list = create_available_ticket_list(results.tickets);
                $('.continue_ticket_purchase_form').after(ticket_list);
            }

        },
        error: function () {
            console.log('js error')
        }
    });
}

function create_form_content(selected_ticket) {
    var container = document.createElement('div');
    container.className = 'form-container';
    container.id = 'already_buying';

    var info_text_element = document.createElement('p');
    info_text_element.className = 'available_ticket_form_content';
    info_text_element.innerText = 'You are already in the process of buying a ticket. Would you like to continue, or select a different ticket';

    var ticket_info_element = document.createElement('p');
    ticket_info_element.className = 'available_ticket_form_content';
    ticket_info_element.innerText = 'Price of the ticket you are buying: \u20AC ' + selected_ticket.price;

    var continue_button = document.createElement('button');
    continue_button.name = 'continue';
    continue_button.className = 'btn btn-success';
    continue_button.innerText = 'Continue with selected ticket';

    var different_ticket_button = document.createElement('a');
    different_ticket_button.href = '/buy-ticket/cancel-ticket/' + selected_ticket.id + '/';
    different_ticket_button.className = 'btn btn-primary';
    different_ticket_button.innerText = 'Select a different ticket';

    container.append(info_text_element);
    container.append(ticket_info_element);
    container.append(continue_button);
    container.append(different_ticket_button);

    $('.continue_ticket_purchase_form').append(container);

}


function ticket_removed_message() {
    var message = document.createElement('div');
    message.innerText = "If you were in the process of buying a ticket and it's gone, it means you you took too long to buy the ticket. Please select a ticket again, and this time try to be a bit quicker ;-)";
    message.className = "alert alert-info";
    message.id = 'ticket_removed_message';

    $('#ticket_removed_message').remove();
    $('.messagelist').append(message);
}


function create_available_ticket_list(tickets) {
    var ticket_list = document.createElement('div');
    ticket_list.className = 'list-group';

    ticket_list = append_available_ticket_header(ticket_list, tickets);
    ticket_list = append_available_ticket_items(ticket_list, tickets);

    return ticket_list
}

function append_available_ticket_header(ticket_list, tickets) {
    var ticket_list_header = document.createElement('h2');
    ticket_list_header.className = 'list-group-item available-tickets-heading';
    ticket_list_header.innerText = 'Available Tickets';

    if (tickets.length == 0) {
        ticket_list_header.innerText = 'No tickets available at the moment'
    }

    ticket_list.appendChild(ticket_list_header);

    return ticket_list
}

function append_available_ticket_items(ticket_list, tickets) {

    for (var i=0; i < tickets.length; i++ ) {
        var ticket_item = create_available_ticket_item(tickets[i]);

        ticket_list.appendChild(ticket_item);
    }

    return ticket_list

}

function create_available_ticket_item(ticket){

    var ticket_item = document.createElement('a');

    var ticket_link = "/buy-ticket/potential_buyer_check/" + ticket.id + '/';
    ticket_item.setAttribute('href', ticket_link);
    ticket_item.className = 'list-group-item available-tickets-item';

    var ticket_item_heading = document.createElement('h3');
    ticket_item_heading.className = 'list-group-item-heading available-tickets-item-heading';
    ticket_item_heading.innerHTML = '&euro; ' + ticket.price;
    ticket_item_heading.style.color = '#0081db';

    var ticket_item_text = document.createElement('p');
    ticket_item_text.className = 'list-group-item-text available-tickets-item-text';
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
    start_get_available_tickets_js();
    // reload_page();
});