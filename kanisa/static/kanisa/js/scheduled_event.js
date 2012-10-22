$(function() {
    var last_automatic_event_title = ''

    $("#id_event").change(function() {
        var selection = $(this).find(":selected").text();

        if ($(this).val().length == 0) {
            // Presumably we've selected the default (null) option,
            // let's reset to the empty string (don't want a title
            // full of dashes).
            selection = '';
        }

        var title_input = $("#id_title");

        if (title_input.val() != last_automatic_event_title) {
            return;
        }

        title_input.val(selection);
        last_automatic_event_title = selection;
    });
});
