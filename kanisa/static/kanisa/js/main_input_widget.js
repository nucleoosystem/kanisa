function get_container(el) {
    return $(el.parents("div.main_input_widget_container")[0]);
}

function get_matching_elements(src, selector) {
    var container = get_container(src);
    return container.find(selector);
}

function show_spinner(el) {
    get_matching_elements(el, ".spinner_placeholder").show();
}

function hide_spinner(el) {
    get_matching_elements(el, ".spinner_placeholder").hide();
}

function get_placeholder(el) {
    return get_matching_elements(el, ".selection_placeholder");
}

function get_cancel(el) {
    return get_matching_elements(el, ".main_input_widget_cancel");
}

function clear_placeholder(event) {
    event.preventDefault();

    var thelink = $(this);
    thelink.hide();

    var other_buttons = get_matching_elements(thelink, ".main_input_widget_action");
    other_buttons.show();

    var placeholder = get_placeholder(thelink);
    placeholder.html("");
}

function hide_alignment(event) {
    get_matching_elements($(this), ".alignment").hide();
}

function show_alignment(event) {
    get_matching_elements($(this), ".alignment").show();
}

function select_image(event) {
    event.preventDefault(event);

    var theimage = $(this);
    var detail_url = theimage.attr("data-select-url");
    var placeholder = get_placeholder(theimage);
    show_spinner(placeholder);

    $.get(detail_url,
          function(data) {
              placeholder.html(data);
              get_matching_elements(placeholder, ".headline_radio").click(hide_alignment);
              get_matching_elements(placeholder, ".medium_radio").click(show_alignment);
              hide_spinner(placeholder);
          });
}

function get_images(event) {
    event.preventDefault();

    var thelink = $(this);
    thelink.hide();

    var theurl = thelink.attr("data-url");
    var placeholder = get_placeholder(thelink);
    show_spinner(thelink);

    $.get(theurl,
          function(data) {
              get_cancel(thelink).show();
              placeholder.html(data);
              $(".main_input_widget_image_choice").click(select_image);
              hide_spinner(thelink);
          });
}

$(function() {
    $(".main_input_widget_insert_image").click(get_images);
    $(".main_input_widget_cancel").click(clear_placeholder);
});
