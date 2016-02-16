function sitewidenotice_close() {
    $('#sitewidenotice').remove();
}

$(document).ready(function() {
    $('.sitewidenotice_close').click(sitewidenotice_close);
});
