$(function() {
    $(".biblepassagewidget").focusout(function() {
        var el = $(this);
        var input = el.val();

        if (el.siblings(".biblepassageresponse").length == 0) {
            el.after("<span class=\"biblepassageresponse\"></span>");
        }

        var status_element = el.siblings(".biblepassageresponse")

        if (input.length == 0) {
             status_element.html('');
            return;
        }

        $.post("/manage/xhr/passage/", { passage: input },
               function(data) {
                   status_element.html('<i class="icon-ok"></i> ' + data);
               }).error(function(data) {
                            status_element.html('<i class="icon-exclamation-sign"></i> ' + data.responseText);
                        });
    });
});
