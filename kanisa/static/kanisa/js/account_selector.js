$(function() {
    $(".kanisaaccountmultipleselector").chosen({
        placeholder_text_multiple: "Select some users"
    });
    $(".kanisaaccountmultipleselector")
        .siblings(".chosen-container")
        .width("100%");
});
