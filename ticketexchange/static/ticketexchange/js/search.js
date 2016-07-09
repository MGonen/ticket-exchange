

function ajax_search_results() {

    search_query = $('#search_input').val();
    no_space_query = search_query.replace(/ /g, '');

    if (no_space_query == '') {
        $('.list-group').remove();
    }
        
    else {
        url = '/get_search_results/' + search_query;

        $.ajax({
            url: url,
            type: "GET",
            success: function(results) {
                $('.list-group').remove();
                events = results.events;
                var event_list = document.createElement('div');
                event_list.className = 'list-group';

                for (var i=0; i < events.length; i++ ){
                    var event_item = document.createElement('a');

                    var event_link = "event/" + events[i].id + '/tickets/';
                    event_item.setAttribute('href', event_link);
                    event_item.className = 'list-group-item';

                    var event_item_heading = document.createElement('h4');
                    event_item_heading.className = 'list-group-item-heading';
                    event_item_heading.innerText = events[i].name;
                    event_item_heading.style.color = '#0081db';

                    var event_item_text = document.createElement('p');
                    event_item_text.className = 'list-group-item-text';
                    event_item_text.innerText = events[i].start_date +', '+ events[i].location;
                    event_item.appendChild(event_item_heading);
                    event_item.appendChild(event_item_text);

                    event_list.appendChild(event_item)
                }
                $('.search_bar').after(event_list);
                // document.body.appendChild(event_list)
            },
            error: function () {
                console.log('js error')
            }
        });
    }

}

// <div class="list-group">
//     <a href="#" class="list-group-item active">
//       <h4 class="list-group-item-heading">First List Group Item Heading</h4>
//       <p class="list-group-item-text">List Group Item Text</p>
//     </a>


/**************************************************************/
/* Shows the link when hovering on it                         */
/**************************************************************/
function find_as_you_type() {
    $('#search_input').keyup(function() {
        ajax_search_results(search_query)
    })
}




function update_search_results() {
    ajax_search_results()
}


/**************************************************************/
/* Functions to execute on loading the document               */
/**************************************************************/
$(document).ready( function() {
    update_search_results();
    find_as_you_type();
});