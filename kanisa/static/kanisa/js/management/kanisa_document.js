/* global update_diary_url:false, schedule_event_url:false, alert_failure: false */

function lookup_documents(evt) {
    console.log("Hello, world");
    var el = $(this);
    var current_val = el.val();

    // Require at least three characters to start doing lookups
    if (current_val.length < 3) {
        return;
    }

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
