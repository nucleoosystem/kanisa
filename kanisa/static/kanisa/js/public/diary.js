/* jshint jquery: true, browser: true */

function bind_previous_week_and_next_week_controls() {
    $(".week_pager").click(update_this_week_table);
}

function update_this_week_table(event) {
    event.preventDefault();

    var el=$(this);

    $.get(update_this_week,
          {'start_date': el.attr("data-date")},
          function(data) {
              $("#this_week_table").html(data);
              bind_previous_week_and_next_week_controls();
          });
}

$(document).ready(function() {
    bind_previous_week_and_next_week_controls();
});
