/* exported popup_closed,open_popup */

var on_popup_close = function() {};

function popup_closed() {
    on_popup_close();
}

function open_popup(url) {
    var newwindow = window.open(url,'name','height=400,width=524');

    if (window.focus) {
        newwindow.focus();
    }

    return false;
}
