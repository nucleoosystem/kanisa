/* global update_regular_events_list:false */

function update_list_of_regular_events(event) {
    event.preventDefault();

    var link = $(this);
    var category_pk = link.attr("data-cat-id");

    $.get(update_regular_events_list,
          {'category': category_pk},
          function(data) {
              $("#regular_event_list").html(data);
          });

    // Remove other active class
    link.parent().parent().find(".active").removeClass("active");

    // Add active class on clicked link
    link.parent().addClass("active");
}

$(document).ready(function() {
    $(".event_category_filter").click(update_list_of_regular_events);
});
