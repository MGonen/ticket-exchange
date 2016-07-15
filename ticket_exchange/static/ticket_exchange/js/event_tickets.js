
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
        success: function(results) {
            $('.list-group').remove();
            var ticket_list = create_event_ticket_list(results.tickets);
            $('.event-details').after(ticket_list);
        },
        error: function () {
            console.log('js error')
        }
    });
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

    var ticket_link = "/buy-ticket/ticket-details/" + ticket.id + '/';
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




/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    // ajax_event_tickets_call();
});