$(document).on('change', '.zipextract.file_tree .folder input[type=checkbox]', function(event) {
  var state = $(this).is(':checked');
  $(this).parent('li').find('ul > li > input[type=checkbox]').selected(state);
});
