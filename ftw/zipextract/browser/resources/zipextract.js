$(document).on('change', '.zipextract.file_tree .folder input[type=checkbox]', function(event) {
  var state = $(this).is(':checked');
  $(this).parent('li').find('ul > li > input[type=checkbox]').selected(state);
});

$(document).on('change', 'form.zipextract input#select_all', function(event) {
  var state = $(this).is(':checked');
  $('form.zipextract .file_tree input[type=checkbox]').selected(state);
});

$(document).on('change', 'form.zipextract .file_tree input[type=checkbox]', function(event) {
  var file_checkboxes = $('form.zipextract .file_tree .file input[type=checkbox]');
  var checked = file_checkboxes.filter(':checked').length;
  var not_checked = file_checkboxes.filter(':not(:checked)').length;
  var select_all = $('form.zipextract input#select_all')[0];
  if(checked === 0) {
    select_all.checked = false;
    select_all.indeterminate = false;
  } else if (not_checked === 0) {
    select_all.checked = true;
    select_all.indeterminate = false;
  } else {
    select_all.checked = false;
    select_all.indeterminate = true;
  }
});
