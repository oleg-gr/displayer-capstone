$(function(){ //DOM Ready

    $(window).bind('resize', function () {
        updatePhotoHeight();
    });

    var updatePhotoHeight = function() {
        var height = $(window).height();
        $.each($("#carousel .carousel-inner div :first-child"), function (index, value) {
           $(this).css('height', height);
        });
    }

    var makeVideo = function(url, type) {
        var format = url.substr(url.lastIndexOf('.') + 1);
        var element = "<video "+ url + "><source src='"+url+"' type='video/"+format+"'>Your browser does not support the video tag.</video>"
        element = "<div class='item' data-type="+ type + ">" + element + '</div>';
        $("#carousel .carousel-inner").append(element);
    }

    var makePicture = function(url, type, duration) {
        element = "<img src=" + url + ">"
        element = "<div class='item' data-type="+ type + " data-duration='" + duration*1000 + "'>" + element + '</div>';
        $("#carousel .carousel-inner").append(element);
    }

    var start_call = function (value, my_id, id_to_call) {

        var peer = new Peer(my_id, {key: 'hx8wr42ud1mj9k9', debug: 3, config: {'iceServers': [
          { url: 'stun:stun.l.google.com:19302' } // Pass in optional STUN and TURN server for maximum network compatibility
        ]}});

        peer.on("open", function (id) {
            console.log("Opened peer with id " + id);
            if (my_id == value["options"]["screens"]["value"][1]) {
                console.log("Trying to call");
                var call = peer.call(id_to_call, window.localStream);
                step3(call);
            }
        });

        peer.on("error", function (err) {
            console.log(err);
        });

        // Receiving a call
        peer.on('call', function(call){
            console.log('Got a call');
            call.answer(window.localStream);
            step3(call);
        });

        function step3 (call) {
          // Hang up on an existing call if present
          if (window.existingCall) {
            window.existingCall.close();
          }

          // Wait for stream on the call, then set peer video display
          call.on('stream', function(stream){
            $('#their-video').prop('src', URL.createObjectURL(stream));
          });

          window.existingCall = call;
        }

    }

    var makePortal = function(value, my_id) {

        var element = '<video id="their-video" autoplay=""></video>';

        element = "<div class='item'>" + element + '</div>';
        $("#carousel .carousel-inner").append(element);

        var id_to_call = value["options"]["screens"]["value"][0] == my_id ? value["options"]["screens"]["value"][1] : value["options"]["screens"]["value"][0];
        console.log("my_id: " + my_id + "; id_to_call: " + id_to_call);

        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

        step1();

        function step1 () {
          // Get audio/video stream
          navigator.getUserMedia({audio: true, video: true}, function(stream){
            window.localStream = stream;
            start_call(value, my_id, id_to_call);
          }, function(){ console.log("error setting up stream") });
        }

    }

    var getInterval = function(elem) {
        return $('div.item.active').data("duration");
    }

    $.getJSON( '/display_data', function (data) {
        if (data["tasks"].length == 0) {
            $("#no-data").show();
        } else {
            $("#no-data").hide();
            var tasks = data['tasks'];
            $.each(tasks, function (index, value) {
                var element, type, duration;
                type = parseInt(value['type']);
                duration = parseInt(value['options']['duration']);
                if (type == 1) {
                // Picture
                    makePicture(value['media'][0], type, duration);
                } else if (type == 4) {
                // Slideshow
                    for (var i = 0; i < value['media'].length; i++) {
                        makePicture(value['media'][i], type, duration);
                    }
                } else if (type == 2) {
                // Video
                    makeVideo(value['media'][0], type);
                } else if (type == 5) {
                    makePortal(value, data["id"]);
                    return;
                }
            });

            $("#carousel .carousel-inner :first").addClass("active");

            $('.carousel').carousel({
                interval:false
            });

            $('#carousel').on('slid.bs.carousel', function () {
                var type = $('div.item.active').data("type");
                if (type == 2) {
                    console.log("video");
                    var video = $('div.item.active video');
                    video.get(0).play();
                    video.get(0).onended = function (e) {
                        $('.carousel').carousel('next');
                    }
                } else {
                    console.log("pictures");
                    setTimeout(function() {
                        $('.carousel').carousel('next');
                    }, getInterval());
                }
            });

            updatePhotoHeight();

            if ($('.carousel-inner .item').length == 1) {
                var type = data["tasks"][0]["type"];
                if (type == 2) {
                    var video = $('div.item.active video');
                    $(video).attr("loop", "loop");
                    video.get(0).play();
                }
            } else {
                $('.carousel').carousel("next");
            }
        }
    });
});