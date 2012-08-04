function update_page_list() {
    $.get(pages_list_url,
          function(data) {
              $("#page_details_container").html(data);
          });
}

$(function() {
    $("#page_quick_create").submit(function() {
        var form = $(this);
        var title_element = form.find("#id_title");
        var title = title_element.val();
        var status_block = form.find("div");
        status_block.html("<i class=\"spinner\"></i>");

        $.post(page_create_url,
               { 'title': title,
                 'parent': '' },
               function(data) {
                   status_block.html("<i class=\"icon-ok\"></i> " + data);
                   title_element.val("");
                   update_page_list();
               }).error(function(data) {
                   status_block.html("<i class=\"icon-exclamation-sign\"></i> " + data.responseText);
               });

        return false;
    });
});
