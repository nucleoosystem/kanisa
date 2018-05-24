/* global update_diary_url:false, schedule_event_url:false, alert_failure: false */

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

$(document).ready(function() {
    $("#document_form #id_search").on('input', lookup_documents);
});
