function get_placeholder_from_link(thelink) {
    return $(thelink.parents("div")[0]).find(".selection_placeholder");
}

function clear_placeholder(event) {
    event.preventDefault();

    var thelink = $(this);
    thelink.hide();

    var other_buttons = thelink.siblings(".main_input_widget_action");
    other_buttons.show();

    var placeholder = get_placeholder_from_link(thelink);
    placeholder.html("");
}

function get_images(event) {
    event.preventDefault();

    var thelink = $(this);
    var cancel_button = thelink.siblings(".main_input_widget_cancel");
    cancel_button.show();
    thelink.hide();

    var theurl = thelink.attr("data-url");
    var placeholder = get_placeholder_from_link(thelink);

    $.get(theurl,
          function(data) {
              placeholder.html(data);
          });
}

$(function() {
    $(".main_input_widget_insert_image").click(get_images);
    $(".main_input_widget_cancel").click(clear_placeholder);
});
