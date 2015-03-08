var interval = 15000;

function doAjax() {
    $.ajax({
            type: 'GET',
            url: '/display_heartbeat',
            complete: function (data) {
                    // Schedule the next
                    setTimeout(doAjax, interval);
            }
    });
}

$(function(){ //DOM Ready

    // Update every 15 seconds
    doAjax();

});