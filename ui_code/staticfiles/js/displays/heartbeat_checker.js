var interval = 10000;

function doHeartbeatCheck() {
    $.getJSON( '/displays_login_info', function (data) {
                    $("table#displays_list tbody tr").each( function () {
                        var id = $(this).data("id");
                        var seconds = data[id];
                        if (seconds <= 30) {
                            $(this).attr('class', 'success');
                            $(this).find(".active_display").text("Active now");
                        } else {
                            $(this).attr('class', 'danger');
                            if (seconds <= 60*2) {
                                warningMessage(this, "1 minute");
                            } else if (seconds <= 60*60) {
                                warningMessage(this, Math.round(seconds/60) + " minutes");
                            } else if (seconds <= 60*60*2) {
                                warningMessage(this, "1 hour");
                            } else if (seconds <= 60*60*24) {
                                warningMessage(this, Math.round(seconds/(60*60)) + " hours");
                            } else if (seconds <= 60*60*24*2) {
                                warningMessage(this, "1 day");
                            } else {
                                warningMessage(this, Math.round(seconds/(60*60*24)) + " days");
                            }
                        }
                    });
                    // Schedule the next
                    setTimeout(doHeartbeatCheck, interval);
                });
}

function warningMessage(obj, time ) {
    $(obj).find(".active_display").html("Active around " + time + " ago<br>Might indicate a problem");
}

$(function(){ //DOM Ready

    // Update every interval seconds
    doHeartbeatCheck();

});