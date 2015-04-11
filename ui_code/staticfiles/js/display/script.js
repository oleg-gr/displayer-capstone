$(function(){ //DOM Ready

    // Update every interval seconds

    var makeElement = function(url, duration) {
        element = "<img src=" + url + " width='100%' height='100%'>"
        return "<div class='item' duration='" + duration*1000 + "'>" + element + '</div>'
    }

    $.getJSON( '/display_data', function (data) {
                    var tasks = data['tasks'];
                    console.log(tasks);
                    $.each(tasks, function (index, value) {
                        var element =  makeElement(value['media'][0], parseInt(value['options']['duration']));
                        console.log(element);
                        $("#carousel .carousel-inner").append(element);
                    });

                    $("#carousel .carousel-inner :first").addClass("active");

                    $('.carousel').carousel({
                        interval:false
                    });

                    setTimeout(function() {
                        $('.carousel').carousel('next');
                    }, parseInt(data['tasks'][0]['options']['duration'])*1000);

                    $('#carousel').on('slide.bs.carousel', function () {
                        var interval = $('div.item.active').attr('duration');
                        console.log(interval);
                        setTimeout(function() {
                            $('.carousel').carousel('next');
                        }, interval);
                    });
                });

});