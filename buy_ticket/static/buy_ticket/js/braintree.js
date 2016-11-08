
function setupBraintreeAjax() {

    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/buy-ticket/payment/token/',
        success: function (results) {
            braintree.setup(results.token, 'dropin', {
                container: 'dropin-container'
            })
        },
        error: function () {
            console.log('js error')
        }
    });
}

function setupBraintree(token) {
    console.log('arrived at js');
    braintree.setup(token, 'dropin', {
        container: 'dropin-container'
    })

}