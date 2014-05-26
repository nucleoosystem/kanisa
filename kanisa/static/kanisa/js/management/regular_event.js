/* jshint jquery: true, browser: true */

$(document).ready(function() {
    $(".regulareventform #id_categories").chosen({
        placeholder_text_multiple: "Select some event categories"
    });
    $(".regulareventform #id_categories")
        .siblings(".chosen-container")
        .width("100%");
    $(".regulareventform #hint_id_categories").hide();
});
