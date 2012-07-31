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

    $(".kanisa_user_perm").change(function() {
        checkbox = $(this);

        perm_id = checkbox.attr("data-permission-id");
        user_id = checkbox.attr("data-user-id");
        assigned = checkbox.attr("checked") == "checked";
        spinner_id = "spinner-" + perm_id.replace(".", "_");

        checkbox.hide();

        checkbox.after("<i class=\"spinner\" id=\"" + spinner_id + "\"></i>");
        spinner = $("#" + spinner_id);

        $.post(permission_change_url,
               { 'permission': perm_id,
                 'user': user_id,
                 'assigned': assigned },
               function(data) {
                   spinner.remove();
                   checkbox.show();
               }).error(function(data) {
                   alert_failure(data.responseText);

                   if (assigned) {
                       checkbox.removeAttr("checked");
                   }
                   else {
                       checkbox.attr("checked", "checked");
                   }

                   spinner.remove();
                   checkbox.show();
               });
    });
});
