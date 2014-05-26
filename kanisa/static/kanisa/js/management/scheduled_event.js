/* jshint jquery: true, browser: true */

function on_event_type_selection_change() {
    // This function sets the event title to the name of the selected
    // event type, every time the event type is changed, unless the
    // event title has been manually edited.

    var selection = $(this).find(":selected").text();

    if ($(this).val().length == 0) {
        // Presumably we've selected the default (null) option,
        // let's reset to the empty string (don't want a title
        // full of dashes).
        selection = '';
    }

    var title_input = $("#id_title");

    // Don't overwrite things the user has manually changed.
    var last_automatic_value = title_input.attr("data-last-automatic-value");

    if (typeof last_automatic_value != "undefined" && title_input.val() != last_automatic_value) {
        return;
    }

    title_input.val(selection);
    title_input.attr("data-last-automatic-value", selection);
}

function on_event_multi_day_change() {
    if ($(this).is(":checked")) {
        $("#div_id_duration").slideUp();
        $("#div_id_end_date").slideDown();
        $("#id_duration").val("");
    }
    else {
        $("#div_id_duration").slideDown();
        $("#div_id_end_date").slideUp();
        $("#id_end_date").val("");
    }
}

function set_initial_multiday_state() {
    var start_date = $("#id_date").val();
    var end_date = $("#id_end_date").val();

    if (start_date != end_date && end_date.length > 0) {
        $("#id_is_multi_day").attr("checked", "checked");
        $("#div_id_duration").hide();
    }
    else {
        $("#id_is_multi_day").removeAttr("checked");
        $("#div_id_end_date").hide();
        $("#id_end_date").val("");
    }
}

$(document).ready(function() {
    $(".scheduledevent #id_event").change(on_event_type_selection_change);
    $(".scheduledevent #id_is_multi_day").change(on_event_multi_day_change);

    if ($('#id_is_multi_day').length != 0) {
        set_initial_multiday_state();
    }
});
