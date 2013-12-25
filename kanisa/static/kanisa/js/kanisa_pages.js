function update_page_list() {
    $.get(pages_list_url,
          function(data) {
              $("#page_details_container").html(data.page_table);
              bind_delete_handlers();

              var parent = $("#id_parent");
              var previous_val = parent.val();
              parent.html(data.options)
              parent.val(previous_val);
          }, "json");
}

function quick_page_create(event) {
    event.preventDefault();

    var form = $(this);

    if (form.data('submitting') == true) {
        return false;
    }

    form.data('submitting', true);

    var title_element = form.find("#id_title");
    var parent_element = form.find("#id_parent");
    var title = title_element.val();
    var status_block = form.find("div");

    status_block.html("<i class=\"spinner\"></i>");

    $.post(page_create_url,
           { 'title': title,
             'parent': parent_element.val() },
           function(data) {
               status_block.html("<i class=\"icon-ok\"></i> " + data);
               title_element.val("");
               update_page_list();
           }).error(function(data) {
               status_block.html("<i class=\"icon-exclamation-sign\"></i> " + data.responseText);
           }).complete(function() {
               form.data('submitting', false);
           });
}

function quick_page_delete(event) {
    event.preventDefault();
    page = $(this).attr("data-page-title");
    if (confirm("Are you sure you want to delete the page \"" + page + "\"?")) {
        $.post($(this).attr("href"),
               function(data) {
                   update_page_list();
               });
    }
}

function bind_delete_handlers() {
    $("a.page_delete").click(quick_page_delete);
}

$(document).ready(function() {
    $("#page_quick_create").submit(quick_page_create);
    bind_delete_handlers();
});
