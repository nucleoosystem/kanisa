function on_user_checkbox_change(event) {
    var checkbox = $(this);

    var perm_id = checkbox.attr("data-permission-id");
    var user_id = checkbox.attr("data-user-id");
    var assigned = checkbox.attr("checked") == "checked";
    var spinner_id = "spinner-" + perm_id.replace(".", "_");

    checkbox.hide();

    checkbox.after("<i class=\"spinner\" id=\"" + spinner_id + "\"></i>");
    var spinner = $("#" + spinner_id);

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
}

$(function() {
    $(".kanisa_user_perm").change(on_user_checkbox_change);
});
