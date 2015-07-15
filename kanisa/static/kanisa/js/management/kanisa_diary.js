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

function quick_event_delete(event) {
    event.preventDefault();
    var title = $(this).attr("data-event-title");
    if (confirm("Are you sure you want to cancel the event \"" + title + "\"?")) {
        $.post($(this).attr("href"),
               function(data) {
                   update_event_list();
               });
    }
}

function bind_diary_handlers() {
    $("a.regular_schedule").click(quick_event_schedule);
    $("a.scheduled_event_cancel").click(quick_event_delete);
}

$(document).ready(function() {
    bind_diary_handlers();

    $("#schedule-weeks-events").mouseover(function() {
        $(".noautoschedule").fadeTo('fast', 0.3);
      }).mouseout(function() {
        $(".noautoschedule").fadeTo('fast', 1.0);
    });
});
