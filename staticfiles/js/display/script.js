$(function(){ //DOM Ready

    var old_data;

    $(window).bind('resize', function () {
        updatePhotoHeight();
    });

    var updatePhotoHeight = function() {
        var height = $(window).height();
        $.each($("#carousel .carousel-inner div :first-child"), function (index, value) {
            $(this).css('height', height);
        });
    }

    var makeVideo = function(task_id, url, type) {
        var format = url.substr(url.lastIndexOf('.') + 1);
        var element = "<video "+ url + "><source src='"+url+"' type='video/"+format+"'>Your browser does not support the video tag.</video>"
        element = "<div class='item' data-type="+ type + " id=" + task_id + ">" + element + '</div>';
        $("#carousel .carousel-inner").append(element);
    }

    var makePicture = function(task_id, url, type, duration) {
        element = "<img src=" + url + ">"
        element = "<div class='item' data-type="+ type + " data-duration='" + duration*1000 + "' id=" + task_id + ">" + element + '</div>';
        $("#carousel .carousel-inner").append(element);
    }

    var start_call = function (value, my_id, id_to_call) {

        var peer = new Peer(my_id, {key: 'hx8wr42ud1mj9k9', debug: 3, config: {'iceServers': [
          { url: 'stun:stun.l.google.com:19302' } // Pass in optional STUN and TURN server for maximum network compatibility
        ]}});

        function tryCalling() {
            console.log(window.existingCall);
            if (!window.existingCall || !window.existingCall.open) {
                console.log("trynna call");
                var call = peer.call(id_to_call, window.localStream);
                step3(call);
            }
            setTimeout(tryCalling, 1000);
        }

        peer.on("open", function (id) {
            console.log("Opened peer with id " + id);
            if (my_id == value["options"]["screens"]["value"][1]) {
                console.log("Trying to call");
                tryCalling();
            }
        });

        peer.on("disconnect", function () {
            function tryReconnecting() {
                if (peer.disconnected) {
                    peer.reconnect();
                    setTimeout(tryReconnecting, 2000);
                }
            }
            tryReconnecting();
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

    }

    var makePortal = function(value, my_id) {

        var element = '<video id="their-video" autoplay=""></video>';

        element = "<div class='item'>" + element + '</div>';
        $("#carousel .carousel-inner").append(element);

        var id_to_call = value["options"]["screens"]["value"][0] == my_id ? value["options"]["screens"]["value"][1] : value["options"]["screens"]["value"][0];
        console.log("my_id: " + my_id + "; id_to_call: " + id_to_call);

        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

        step1(value, my_id, id_to_call);

    }

    var step1 = function (value, my_id, id_to_call) {
          // Get audio/video stream
          navigator.getUserMedia({audio: true, video: true}, function(stream){
            window.localStream = stream;

            start_call(value, my_id, id_to_call);

          }, function(){ console.log("error setting up stream") });
        }

    var step3 = function (call) {
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

    var getInterval = function(elem) {
        return $('div.item.active').data("duration");
    }

    var processData = function(data) {
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
                    makePicture(value['id'], value['media'][0], type, duration);
                } else if (type == 4) {
                // Slideshow
                    for (var i = 0; i < value['media'].length; i++) {
                        makePicture(value['id'], value['media'][i], type, duration);
                    }
                } else if (type == 2) {
                // Video
                    makeVideo(value['id'], value['media'][0], type);
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
                        console.log("video next");
                        $('.carousel').carousel('next');
                    }
                } else {
                    console.log("pictures");
                    setTimeout(function() {
                        console.log("pic next");
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
                setTimeout(function() {
                    $('.carousel').carousel('next');
                }, getInterval());
            }
        }
    }

    $.getJSON( '/display_data', function (data) {
        processData(data);
        old_data = data;
        setTimeout(function() {
            updateJson();
        }, 3000);
    });

    function arr_diff(a1, a2)
    {
      var a=[], diff=[];
      for(var i=0;i<a1.length;i++)
        a[a1[i]]=true;
      for(var i=0;i<a2.length;i++)
        if(a[a2[i]]) delete a[a2[i]];
        else a[a2[i]]=true;
      for(var k in a)
        diff.push(k);
      return diff;
    }

    var updateJson = function() {
        $.getJSON( '/display_data', function (data) {
            console.log("updating_  json");
            console.log(data);
            console.log(old_data);
            console.log("1111");
            if (data["tasks"].toString() != old_data["tasks"].toString()) {
                console.log("if triggered");
                $('.carousel-inner .item').remove();
                $('#carousel').off('slid.bs.carousel');
                var id = window.setTimeout(function() {}, 0);

                while (id--) {
                    window.clearTimeout(id); // will do nothing if no timeout with id is present
                }
                processData(data);
            }
            // processData(data);
            old_data = data;
            setTimeout(updateJson, 3000);
        });
    }
});