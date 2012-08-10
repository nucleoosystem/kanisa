function update_event_list() {
    $.get(update_diary_url,
          function(data) {
              $("#diary_page").html(data);
              bind_diary_handlers();
          });
}

function quick_event_schedule(event) {
    event.preventDefault();
    var el = $(this);
    el.hide();
    var status_block = el.siblings("span");
    var event_id = el.attr("data-event-id");
    var date = el.attr("data-event-date");

    status_block.html("<i class=\"spinner\"></i>");

    $.post(schedule_event_url, {'event': event_id, 'date': date},
           function(data) {
               update_event_list();
           }).error(function(data) {
               alert_failure(data.responseText);
               el.show();
               status_block.html('');
           });
}

function bind_diary_handlers() {
    $("a.regular_schedule").click(quick_event_schedule);
}

$(function() {
    bind_diary_handlers();
});
