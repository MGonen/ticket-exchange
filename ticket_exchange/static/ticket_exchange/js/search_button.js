
function searchButtonDisabled() {
    $('#search_input').on('input', handleChange);

}

function handleChange(e) {
    if (e.target.value.length <= 1) {
        $('#searchButton').prop('disabled', true);
    } else {
        $('#searchButton').prop('disabled', false);
    }
}



$(document).ready( function() {
    searchButtonDisabled()
});