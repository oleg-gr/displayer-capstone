var interval = 15000;

function doHeartbeat() {
    $.ajax({
            type: 'GET',
            url: '/display_heartbeat',
            complete: function (data) {
                    // Schedule the next
                    setTimeout(doHeartbeat, interval);
            }
    });
}

$(function(){ //DOM Ready

    // Update every interval seconds
    doHeartbeat();

});