function on_band_change(event) {
    var selection = $(this).val();

    if ($(this).val().length == 0) {
        // Presumably we've selected the default (null) option,
        // let's reset things.
        $("#id_band_leader").val('');
        $("#id_musicians").val([]);
        return;
    }

    var url = $(this).parents("form").attr("data-band-info-url")

    $.get(
        url,
        {'band_id': selection},
        function(data) {
            $("#id_band_leader").val(data.band_leader);
            $("#id_musicians").val(data.musicians);
            $("#id_musicians").trigger("chosen:updated");
        },
        "json"
    );
}

function on_date_change_evt(event) {
    var el = $(this);

    var warning_div = $("#id_date_warning");

    if (warning_div.length == 0) {
        $(this).after("<div id=\"id_date_warning\" class=\"help-inline\"></div>");
    }

    var url = $(this).parents("form").attr("data-event-info-url")

    $.get(
        url,
        {'date': el.val()},
        function(data) {
            var events_input = $("#id_event");
            var warning_div = $("#id_date_warning");
            warning_div.parents(".control-group").addClass("error");
            var options_html = ''

            if (data.events.length == 0) {
                // Add warning about bad date selection
                warning_div.html("<strong>There are no events on that date.</strong>");
                events_input.html("");
                events_input.parent().parent().hide();
                return;
            }

            // Clear warning about bad date selection
            warning_div.html("");
            warning_div.parents(".control-group").removeClass("error");

            // Remove any error from the events dropdown (which would
            // have been added if we'd posted without filling in an
            // event).
            events_input.parents(".control-group").removeClass("error")
            // Remove help text from the events dropdown (which would
            // have been added if we'd posted without filling in an
            // event).
            events_input.siblings("span").remove();

            for (var i = 0; i < data.events.length; i++) {
                options_html += '<option value="' + data.events[i][0] + '">' + data.events[i][1] + '</option>'
            }

            events_input.html(options_html);
            events_input.parent().parent().show()
        },
        "json"
    );
}

$(function() {
    $("#id_band").change(on_band_change);
    $("#id_date").change(on_date_change_evt);
    $("#id_event").parent().parent().hide();
});
