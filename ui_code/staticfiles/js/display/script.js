$(function(){ //DOM Ready

    $(window).bind('resize', function () {
        updatePhotoHeight();
    });

    var updatePhotoHeight = function() {
        var height = $(window).height();
        console.log("sup");
        $.each($("#carousel .carousel-inner div :first-child"), function (index, value) {
           console.log($(this));
           $(this).css('height', height);
           console.log("heigh " + height);
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
                }
            });

            $("#carousel .carousel-inner :first").addClass("active");

            $('.carousel').carousel({
                interval:false
            });

            if (tasks)

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

            if (data["tasks"].length == 1) {
                if (data["tasks"][0]["type"] == 2) {
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