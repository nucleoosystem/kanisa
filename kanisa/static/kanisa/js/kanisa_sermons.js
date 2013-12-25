function quick_series_complete(event) {
    event.preventDefault();
    var el = $(this);
    el.hide();
    var series = el.attr("data-series-id");
    var status_block = el.siblings("span");

    status_block.html("<i class=\"spinner\"></i>");

    $.post(series_complete_url, {'series': series},
           function(data) {
               el.remove();
               status_block.html('<i class="icon-ok"></i> ' + data);
               status_block.delay(3000).fadeOut(1000);
           }).error(function(data) {
               alert_failure(data.responseText);
               el.show();
               status_block.html('');
           });
}

$(document).ready(function() {
    $("a.series_complete").click(quick_series_complete);
});
