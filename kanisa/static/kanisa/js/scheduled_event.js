$(function() {
    var last_set_value = ''

    $("#id_event").change(function() {
        var selection = $(this).find(":selected").text();

        if ($(this).val().length == 0) {
            // Presumably we've selected the default (null) option,
            // let's reset to the empty string (don't want a title
            // full of dashes).
            selection = '';
        }

        var title_input = $("#id_title");

        if (title_input.val() != last_set_value) {
            return;
        }

        title_input.val(selection);
        last_set_value = selection;
    });
});
