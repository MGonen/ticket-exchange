

function event_search_results() {

    search_query = $('#search_input').val();
    no_space_query = search_query.replace(/ /g, '');

    if (no_space_query == '') {
        $('.list-group').remove();
    }
        
    else {
        ajax_search_call(search_query);
    }
}

function ajax_search_call(search_query) {
    url = '/get_search_results/' + search_query;

    $.ajax({
        url: url,
        type: "GET",
        // async: false,
        success: function(results) {
            $('.list-group').remove();
            var event_list = create_event_search_list(results.events);
            $('.search_bar').after(event_list);
        },
        error: function () {
            console.log('js error')
        }
    });
}

function create_event_search_list(events) {
    var event_list = document.createElement('div');
    event_list.className = 'list-group homepage-search-results';

    event_list = append_event_search_items(event_list, events);

    return event_list
}


function append_event_search_items(event_list, events) {

    for (var i=0; i < events.length; i++ ) {
        var event_item = create_event_search_item(events[i]);

        event_list.appendChild(event_item);
    }

    return event_list

}

function create_event_search_item(event){

    var event_item = document.createElement('a');

    var event_link = "event/" + event.id + '/tickets/';
    event_item.setAttribute('href', event_link);
    event_item.className = 'list-group-item';

    var event_item_heading = document.createElement('h4');
    event_item_heading.className = 'list-group-item-heading';
    event_item_heading.innerText = event.name;
    event_item_heading.style.color = '#0081db';

    var event_item_text = document.createElement('p');
    event_item_text.className = 'list-group-item-text';
    event_item_text.innerText = event.start_date + ', ' + event.location;
    event_item.appendChild(event_item_heading);
    event_item.appendChild(event_item_text);

    return event_item
}


// function supersede_link(){
//     $('body').on("click", 'a.list-group-item', function(){
//
//         // alert('clicked on link');
//         console.log('hover on link');
//
//         return false;
//     })
// }

/**************************************************************/
/* Shows the link when hovering on it                         */
/**************************************************************/
function find_as_you_type() {
    $('#search_input').keyup(function() {
        event_search_results(search_query)
    })
}




function update_search_results() {
    event_search_results()
}


/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    update_search_results();
    find_as_you_type();
    // supersede_link();
});