function _alert_impl(msg, alert_class) {
    var alert_box = $("#kanisa_alerts");
    $(".js-alert").remove();
    var html = "<div class=\"js-alert alert " + alert_class + "\" style=\"display: none\">";
    html += "<button class=\"close\" data-dismiss=\"alert\">&times;</button>" + msg + "</div>";
    alert_box.after(html);
    $(".js-alert").slideDown('fast');
}

function alert_failure(msg) {
    _alert_impl(msg, "alert-danger");
}
