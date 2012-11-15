// This stuff gets us around Django's CSRF verification, in a good
// way.

jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

// Kanisa-specific functionality

function _alert_impl(msg, alert_class) {
    alert_box = $("#kanisa_alerts");
    $(".js-alert").remove();
    html = "<div class=\"js-alert alert " + alert_class + "\" style=\"display: none\">";
    html += "<button class=\"close\" data-dismiss=\"alert\">&times;</button>" + msg + "</div>";
    alert_box.after(html);
    $(".js-alert").slideDown('fast');
}

function alert_success(msg) {
    _alert_impl(msg, "alert-success");
}

function alert_failure(msg) {
    _alert_impl(msg, "alert-error");
}

$(function() {
    $("#schedule-weeks-events").mouseover(function() {
        $(".noautoschedule").fadeTo('fast', 0.3);
      }).mouseout(function(){
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
