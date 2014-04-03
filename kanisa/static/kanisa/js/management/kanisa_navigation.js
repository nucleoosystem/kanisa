function navigation_move(event, el, url) {
   event.preventDefault();

    var element_pk = el.attr("data-navigation-id");
    var parent = el.parent();
    var old_html = parent.html()
    el.parent().html("<i class=\"spinner\"></i>");

    $.post(url, {'navigation_element': element_pk},
           function(data) {
               update_navigation_list();
           }).error(function(data) {
               alert_failure(data.responseText);
               parent.html(old_html);
           });
}

function navigation_move_up(event) {
    navigation_move(event, $(this), navigation_up_url);
}

function navigation_move_down(event) {
    navigation_move(event, $(this), navigation_down_url);
}

function bind_navigation_move_handlers() {
    $("a.move_up").click(navigation_move_up);
    $("a.move_down").click(navigation_move_down);
}

function update_navigation_list() {
    $.get(list_navigation_url,
          function(data) {
              $("#navigation_details_container").html(data);
              bind_navigation_move_handlers();
          });
}

function quick_navigation_delete(event) {
    event.preventDefault();
    var title = $(this).attr("data-navigation-title");
    if (confirm("Are you sure you want to delete the navigation element \"" + title + "\"?")) {
        $.post($(this).attr("href"),
               function(data) {
                   update_navigation_list();
               });
    }
}

function bind_navigation_delete_handlers() {
    $("a.navigation_delete").click(quick_navigation_delete);
}

$(document).ready(function() {
    bind_navigation_move_handlers();
    bind_navigation_delete_handlers();
});
