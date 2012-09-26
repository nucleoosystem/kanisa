function show_spinner(thelink) {
    thelink.siblings(".spinner_placeholder").show();
}

function hide_spinner(thelink) {
    thelink.siblings(".spinner_placeholder").hide();
}

function get_placeholder_from_link(thelink) {
    return $(thelink.parents("div")[0]).find(".selection_placeholder");
}

function get_cancel_from_link(thelink) {
    return thelink.siblings(".main_input_widget_cancel");
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

function select_image(event) {
    event.preventDefault(event);

    var theimage = $(this);
    var detail_url = theimage.attr("data-select-url");
    var placeholder = theimage.parent();

    $.get(detail_url,
          function(data) {
              placeholder.html(data);
          });
}

function get_images(event) {
    event.preventDefault();

    var thelink = $(this);
    thelink.hide();

    var theurl = thelink.attr("data-url");
    var placeholder = get_placeholder_from_link(thelink);
    show_spinner(thelink);

    $.get(theurl,
          function(data) {
              var cancel_button = get_cancel_from_link(thelink);
              cancel_button.show();
              placeholder.html(data);
              $(".main_input_widget_image_choice").click(select_image);
              hide_spinner(thelink);
          });
}

$(function() {
    $(".main_input_widget_insert_image").click(get_images);
    $(".main_input_widget_cancel").click(clear_placeholder);
});
