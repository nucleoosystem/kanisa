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
    } else {
        show_alignment(radio);
    }
}

function insert_image(event) {
    event.preventDefault(event);
    var btn = $(this);
    var image_pk = get_matching_elements(btn, ".main_input_widget_image_choice").attr("data-img-pk");
    var size = get_size(btn);
    var alignment = get_alignment(btn);

    var textarea = get_matching_elements(btn, "textarea");
    var image_code = "![img-" + image_pk + " " + size;

    if (size != "headline") {
        image_code += " " + alignment;
    }

    image_code += "]";

    textarea.insertAtCaret(image_code);

    get_cancel(btn).click();
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
              get_matching_elements(placeholder, "input[name=size]").click(change_size);
              get_matching_elements(placeholder, ".main_input_widget_image_insert").click(insert_image);
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
