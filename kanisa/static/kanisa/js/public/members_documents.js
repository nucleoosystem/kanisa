function lookup_documents(evt) {
    var el = $(this);
    var current_val = el.val();

    $.get(
        "",
        {
            'title': current_val,
        },
        function(data) {
            $("#document_results").html(data);
        }
    ).error(
        function(data) {
            $("#document_results").html(data.responseText);
        }
    );
}

function toggle_document_details(event) {
    event.preventDefault();

    var element = $(this);

    element.toggle();
    var theclass = element.attr("class");

    if (theclass == "document_details_short") {
        element.siblings(".document_details_full").toggle();
    }
    else {
        element.siblings(".document_details_short").toggle();
    }

}

$(document).ready(function() {
    $(".document_details_short").click(toggle_document_details);
    $(".document_details_full").click(toggle_document_details);
    $("#document_form #id_search").on('input', lookup_documents);
});
