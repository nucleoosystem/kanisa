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
              hide_spinner(thelink);
          });
}

$(function() {
    $(".main_input_widget_insert_image").click(get_images);
    $(".main_input_widget_cancel").click(clear_placeholder);
});
