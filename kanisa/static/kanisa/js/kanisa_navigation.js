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

function bind_move_handlers() {
    $("a.move_up").click(navigation_move_up);
    $("a.move_down").click(navigation_move_down);
}

function update_navigation_list() {
    $.get(list_navigation_url,
          function(data) {
              $("#navigation_details_container").html(data);
              bind_move_handlers();
          });
}

$(function() {
    bind_move_handlers();
});


