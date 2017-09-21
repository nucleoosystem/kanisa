/* global update_diary_url:false, schedule_event_url:false, alert_failure: false */

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

function update_diary_modal(event) {
    var element = $(this);
    var yyyymmdd = element.attr("data-date-yyyymmdd");
    var display = element.attr("data-date-display");

    // Update the modal title with the display date
    $("#add_modal_date").html(display);

    // Fix the link for heading straight to add an event
    var btn = $("#add_details_myself");
    var url = btn.attr("href");
    btn.attr("href", url.split('?')[0] + "?date=" + yyyymmdd);

    // Clear out the lookup field
    $("#id_name").val("");
    $("#id_date").val(yyyymmdd);
    $("#possible_events").html("");
}

function lookup_events(evt) {
    var el = $(this);
    var current_val = el.val();

    // Require at least three characters to start doing lookups
    if (current_val.length < 3) {
        $("#possible_events").html("");
        return;
    }

    var event_date = $("#id_date").val()

    $.post(
        find_events_in_diary_url,
        {
            'event_name': current_val,
            'event_date': event_date
        },
        function(data) {
            $("#possible_events").html(data);
        }
    ).error(
        function(data) {
            $("#possible_events").html(data.responseText);
        }
    );
}

function bind_diary_handlers() {
    $("a.regular_schedule").click(quick_event_schedule);
    $("a.scheduled_event_cancel").click(quick_event_delete);
    $("a.diary_modal_toggle").click(update_diary_modal);
}

$(document).ready(function() {
    $("#id_name").on('input', lookup_events);
    bind_diary_handlers();

    $("#schedule-weeks-events").mouseover(function() {
        $(".noautoschedule").fadeTo('fast', 0.3);
      }).mouseout(function() {
        $(".noautoschedule").fadeTo('fast', 1.0);
    });
});
