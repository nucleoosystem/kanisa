function reload_documents(title) {
    $.get(
        "",
        {
            'title': title,
        },
        function(data) {
            $("#document_results").html(data);
            bind_document_expiry_handlers();
        }
    ).error(
        function(data) {
            $("#document_results").html(data.responseText);
        }
    );
}

function lookup_documents(evt) {
    var el = $(this);
    var current_val = el.val();
    reload_documents(current_val);
}

function handle_expiry_toggle(event) {
    event.preventDefault();
    var form = $(this);

    if (form.data('submitting') === true) {
        return false;
    }

    form.data('submitting', true);
    $.post(
        form.attr("action"),
        {},
        function(data) {
            reload_documents($("#id_search").val());
        }).error(function(data) {
            form.data('submitting', false);
        });
}

function bind_document_expiry_handlers() {
    $("form.expiry_toggle").submit(handle_expiry_toggle);
}

$(document).ready(function() {
    $("#document_form #id_search").on('input', lookup_documents);
    bind_document_expiry_handlers();
});
