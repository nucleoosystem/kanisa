jQuery.fn.extend({
    insertAtCaret: function(myValue){
        return this.each(function(i) {
            if (document.selection) {
                // For browsers like Internet Explorer
                this.focus();
                var sel = document.selection.createRange();
                sel.text = myValue;
                this.focus();
            } else if (this.selectionStart || this.selectionStart == '0') {
                // For browsers like Firefox and Webkit based
                var startPos = this.selectionStart;
                var endPos = this.selectionEnd;
                var scrollTop = this.scrollTop;
                this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
                this.focus();
                this.selectionStart = startPos + myValue.length;
                this.selectionEnd = startPos + myValue.length;
                this.scrollTop = scrollTop;
            } else {
                this.value += myValue;
                this.focus();
            }
        })
    }
});

function get_container(el) {
    return $(el.parents("div.main_input_widget_container")[0]);
}

function get_matching_elements(src, selector) {
    return get_container(src).find(selector);
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

    on_popup_close = function() {};
}

function hide_alignment(element) {
    get_matching_elements(element, ".alignment").hide();
}

function show_alignment(element) {
    get_matching_elements(element, ".alignment").show();
}

function get_size(element) {
    return get_matching_elements(element, "input[name=size]:checked").attr("value");
}

function get_alignment(element) {
    return get_matching_elements(element, "input[name=alignment]:checked").attr("value");
}

function change_size(event) {
    var radio = $(this);

    var size = get_size(radio);

    if (size == "headline") {
        hide_alignment(radio);
        get_matching_elements(radio, ".thumbnail-small").hide();
        get_matching_elements(radio, ".thumbnail-medium").hide();
        get_matching_elements(radio, ".thumbnail-headline").show();
    } else if (size == "medium") {
        show_alignment(radio);
        get_matching_elements(radio, ".thumbnail-small").hide();
        get_matching_elements(radio, ".thumbnail-medium").show();
        get_matching_elements(radio, ".thumbnail-headline").hide();
    } else {
        show_alignment(radio);
        get_matching_elements(radio, ".thumbnail-small").show();
        get_matching_elements(radio, ".thumbnail-medium").hide();
        get_matching_elements(radio, ".thumbnail-headline").hide();
    }
}

function get_code(element) {
    var image_pk = get_matching_elements(element, ".main_input_widget_image_choice").attr("data-img-pk");
    var size = get_size(element);

    var image_code = "![img-" + image_pk + " " + size;

    if (size != "headline") {
        image_code += " " + get_alignment(element);
    }

    image_code += "]";

    return image_code;
}

function update_code_preview(element) {
    get_matching_elements(element, ".image-code").html(get_code(element));
}

function on_image_attribute_change(event) {
    update_code_preview($(this));
}

function insert_image(event) {
    event.preventDefault(event);
    var btn = $(this);

    get_matching_elements(btn, "textarea").insertAtCaret(get_code(btn));

    get_cancel(btn).click();
}

function select_image(event) {
    event.preventDefault(event);

    var theimage = $(this);
    var placeholder = get_placeholder(theimage);
    show_spinner(placeholder);

    $.get(theimage.attr("data-select-url"),
          function(data) {
              placeholder.html(data);
              get_matching_elements(placeholder, "input[name=size]").click(change_size);
              get_matching_elements(placeholder, ".main_input_widget_image_insert").click(insert_image);
              get_matching_elements(placeholder, ".main_input_widget_get_images").click(get_images);
              update_code_preview(placeholder);
              get_matching_elements(placeholder, "input[type=radio]").click(on_image_attribute_change);
              hide_spinner(placeholder);
          });
}

function paginate_images(event) {
    event.preventDefault();

    var thelink = $(this);
    var url = thelink.attr("href");
    var placeholder = get_placeholder(thelink);
    refresh_images(placeholder, url);
}

function refresh_images(placeholder, url) {
    show_spinner(placeholder);

    $.get(url,
          function(data) {
              get_cancel(placeholder).show();
              placeholder.html(data);
              get_matching_elements(placeholder, ".main_input_widget_image_choice").click(select_image);
              hide_spinner(placeholder);
              get_matching_elements(placeholder, ".main_input_widget_image_paginate").click(paginate_images);
          });
}

function get_images(event) {
    event.preventDefault();

    var thelink = $(this);
    get_matching_elements(thelink, ".main_input_widget_action").hide();

    var placeholder = get_placeholder(thelink);
    var url = thelink.attr("data-url");

    refresh_images(placeholder, url);

    on_popup_close = function() {
        refresh_images(placeholder, url);
    };
}

function insert_attachment(event) {
    event.preventDefault();
    var document_link = $(this);
    var document_pk = document_link.attr("data-pk");
    var code = "{@document-" + document_pk + "}";
    get_matching_elements(document_link, "textarea").insertAtCaret(code);
    get_cancel(document_link).click();
}

function refresh_attachments(placeholder, url) {
   show_spinner(placeholder);

    $.get(url,
          function(data) {
              get_cancel(placeholder).show();
              placeholder.html(data);
              get_matching_elements(placeholder, ".media-documents a").click(insert_attachment);
              hide_spinner(placeholder);
          });
}

function get_attachments(event) {
    event.preventDefault();

    var thelink = $(this);
    get_matching_elements(thelink, ".main_input_widget_action").hide();

    var placeholder = get_placeholder(thelink);

    var url = thelink.attr("data-url")
    refresh_attachments(placeholder, url);

    on_popup_close = function() {
        refresh_attachments(placeholder, url);
    };
 }

$(function() {
    $(".main_input_widget_insert_image").click(get_images);
    $(".main_input_widget_add_attachment").click(get_attachments);
    $(".main_input_widget_cancel").click(clear_placeholder);
});
