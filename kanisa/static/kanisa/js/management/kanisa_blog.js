function get_rough_word_count(str) {
  return str.split(/\s+/).length;
}

function hide_word_count_warning(element) {
    element.siblings(".word-count-warning").remove();
}

function show_word_count_warning(words, element) {
    hide_word_count_warning(element);
    var contents = "Only the first 30 words will show up on the home page, you've written about " + words + " words.";
    element.after("<p class=\"alert alert-warning word-count-warning\">" + contents + "</p>");
}

function update_word_count_impl(element) {
    var word_count = get_rough_word_count(element.val());
    var help_block = element.parent().parent().children(".help-block")

    if (word_count < 25) {
        hide_word_count_warning(help_block);
    }
    else {
        show_word_count_warning(word_count, help_block);
    }
}

function update_word_counter(evt) {
    var element = $(this);
    update_word_count_impl(element);
}

$(document).ready(function() {
    update_word_count_impl($(".kanisablogteaserinputwidget"));
    $(".kanisablogteaserinputwidget").bind('input propertychange', update_word_counter);
});
