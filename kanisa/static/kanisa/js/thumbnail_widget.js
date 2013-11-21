$(function() {
    var controls_element = $(".thumbnailfileinput").parent();
    var checkbox = controls_element.find("input[type=checkbox]");
    var label = controls_element.find("label");

    checkbox.css("vertical-align", "top").css("margin-top", "10px")
    label.css("vertical-align", "top").css("display", "inline-block").css("margin-top", "6px")
});
