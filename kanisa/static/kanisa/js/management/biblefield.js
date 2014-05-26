$(document).ready(function() {
    $(".biblepassagewidget").focusout(function() {
        var el = $(this);
        var input = el.val();

        if (el.siblings(".biblepassageresponse").length == 0) {
            el.after("<span class=\"biblepassageresponse\"></span>");
        }

        var status_element = el.siblings(".biblepassageresponse");

        if (input.length == 0) {
            status_element.html('');
            return;
        }

        var url = el.attr("data-validate-url");

        if (url === undefined) {
            status_element.html('<i class="icon-exclamation-sign"></i> Could not locate Bible passage checker.');
            return;
        }

        $.post(url, { passage: input },
               function(data) {
                   status_element.html('<i class="icon-ok"></i> ' + data);
               }).error(function(data) {
                   status_element.html('<i class="icon-exclamation-sign"></i> ' + data.responseText);
               });
    });
});
