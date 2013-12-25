$(document).ready(function() {
    $("#schedule-weeks-events").mouseover(function() {
        $(".noautoschedule").fadeTo('fast', 0.3);
      }).mouseout(function() {
        $(".noautoschedule").fadeTo('fast', 1.0);
    });

    $('.carousel').carousel({
        interval: 2000
    });
});

var on_popup_close = function() {};

function popup_closed() {
    on_popup_close();
}

function open_popup(url) {
    var newwindow = window.open(url,'name','height=269,width=524');

    if (window.focus) {
        newwindow.focus();
    }

    return false;
}
