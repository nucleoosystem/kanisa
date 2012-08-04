function update_page_list() {
    $.get(pages_list_url,
          function(data) {
              $("#page_details_container").html(data);
          });
}

function do_nothing() {
    return false;
}

function quick_page_create() {
    var form = $(this);
    form.unbind('submit', quick_page_create);
    form.bind('submit', do_nothing);

    var button = form.find("button");
    button.attr("disabled", "disabled");

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
               button.removeAttr("disabled");
               form.bind('submit', quick_page_create);
               form.unbind('submit', do_nothing);
           }).error(function(data) {
               status_block.html("<i class=\"icon-exclamation-sign\"></i> " + data.responseText);
               button.removeAttr("disabled");
               form.bind('submit', quick_page_create);
               form.unbind('submit', do_nothing);
           });

    return false;
}

$(function() {
    $("#page_quick_create").submit(quick_page_create);
});
