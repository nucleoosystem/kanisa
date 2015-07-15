/* exported update_with_composer */

function update_with_composer(pk, full_name) {
    var the_select = $("#id_composers");
    var selected_values = the_select.val();

    var new_opt = '<option value="' + pk + '">' + full_name + '</option>';
    the_select.html(the_select.html() + new_opt);

    if (selected_values === null) {
        the_select.val(pk);
    }
    else {
        selected_values.push(pk);
        the_select.val(selected_values);
    }
}
