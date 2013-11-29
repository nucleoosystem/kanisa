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
            on_musician_change()
        },
        "json"
    );
}

function get_name(el) {
    return el.innerText;
}

function on_musician_change() {
    var el = $("#id_musicians");
    var selected_musicians = el.children(":selected").toArray()
    var selected_names = selected_musicians.map(get_name);
    var help_block = el.parent().find(".help-block");
    help_block.html("<strong>Currently selected:</strong> " + selected_names.join("; "));
}

function on_musician_change_evt(event) {
    on_musician_change();
}

$(function() {
    $("#id_band").change(on_band_change);
    $("#id_musicians").change(on_musician_change_evt);
});
