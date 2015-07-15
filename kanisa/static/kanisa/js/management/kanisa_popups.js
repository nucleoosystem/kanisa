var on_popup_close = function() {};

function popup_closed() {
    on_popup_close();
}

function open_popup(url) {
    var newwindow = window.open(url,'name','height=269,width=524');

    if (window.focus) {
        newwindow.focus();
    }

    return false;
}
