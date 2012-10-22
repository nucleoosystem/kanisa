function on_event_type_selection_change() {
    // This function sets the event title to the name of the selected
    // event type, every time the event type has changed, unless the
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

    if (typeof last_automatic_value != "undefined" &&  title_input.val() != last_automatic_value) {
        return;
    }

    title_input.val(selection);
    title_input.attr("data-last-automatic-value", selection);
}

$(function() {
    $("#id_event").change(on_event_type_selection_change);
});
