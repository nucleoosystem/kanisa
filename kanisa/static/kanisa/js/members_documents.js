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

$(function() {
    $(".document_details_short").click(toggle_document_details);
    $(".document_details_full").click(toggle_document_details);
});
