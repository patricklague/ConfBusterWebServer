/* 
 * Redirection
 */
function openLinkInNewTab( url )
{
  window.open(url, '_blank');
  window.focus();
}
function goToPage( url )
{
  document.location.href = url;
}
function submitForm()
{
  // Put back the component regular font
  clearErrorMessages();

  // Submit the form if valid
  if(validateEmail() && validateFileType()) 
  {
    changeToProgressCursor();
    $('#form').submit();
  }
}

/*
 * Form Validation
 */
function showWarning(id)
{
  $(id).css({ 'color': '#FF6400' }); // Dark Orange
}
function clearWarning(id)
{
  $(id).css({ 'color': 'black' });
}
function showError(id)
{
  id = '#' + id;
  $(id).fadeOut('fast');
  $(id).fadeIn('slow');
  $(id).css({ 'color': 'red' });
}
function clearErrorMessages()
{
  $('#emailErrorFormat').css({ 'color': 'black' });
  $('#emailErrorLength').css({ 'color': 'black' });

  $('#fileErrorExtension').css({ 'color': 'black' });
  $('#fileErrorSize').css({ 'color': 'black' });
  $('#fileErrorName').css({ 'color': 'black' });
  $('#fileErrorChar').css({ 'color': 'black' });
}

/*
 * Email Validation
 */
function validateEmail()
{
  var email = $('#form_email_input').val();
  email = String(email).toLowerCase();

  return validateEmailFormat(email) && validateEmailLength(email);
}
function validateEmailFormat( email )
{
  var emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  var regexFulfilled = emailRegex.test(email);
    
  if(!regexFulfilled) {
    showError("emailErrorFormat");
  }      

  return regexFulfilled;
}
function validateEmailLength( email )
{
  var lengthIsValid = (email.length <= 50);

  if(!lengthIsValid) {
    showError("emailErrorLength");
  } 
  
  return lengthIsValid;
}

function validateEmailProvider(labelId)
{
  /*
  labelId = '#' + labelId;
  var email = $('#form_email_input').val();
  email = String(email).toLowerCase();

  if (email.indexOf("@gmail") != -1)
    showWarning(labelId);
  else
    clearWarning(labelId);
  */
}


/*
 * File Validation
 */
function validateFileType()
{

  return validateFileChar() && validateFileName() && validateFileExtension() && validateFileSize();
}
function validateFileChar()
{
    var fileName = ($('#form_file_input').val()).replace("C:\\fakepath\\","");

    var fileNameRegex = /^[a-zA-Z0-9_.\-]+\.[a-zA-Z0-9_.\-]+$/; 
    var charAreValid = fileNameRegex.test(fileName);
  
  if(!charAreValid) {
    showError("fileErrorChar");
  } 

  return charAreValid;
}
function validateFileName()
{
  var fileName = ($('#form_file_input').val()).replace("C:\\fakepath\\","");

  var lengthIsValid = (fileName.length <= 50);

  if(!lengthIsValid) {
    showError("fileErrorName");
  } 

  return lengthIsValid;
}
function validateFileExtension()
{
  var fileName = $('#form_file_input').val();

  var extension = $('#form_file_input').val().split('.').pop().toLowerCase();
  var extensionIsValid = $.inArray(extension, ['pdb','sdf','mol','mol2']) != -1;

  if(!extensionIsValid) {
      showError("fileErrorExtension");
  } 

  return extensionIsValid;
}
function validateFileSize()
{
  var maximumFileSize = 1000000; // 1 000 000 o = 1 Mo
  var fileSizeIsValid = (SuperGlobalFileSize > 0) && (SuperGlobalFileSize <= maximumFileSize); 

  if(!fileSizeIsValid) {
    showError("fileErrorSize");
  } 

  return fileSizeIsValid;
}


/* 
 * Cursor style 
 */
function changeToRegularCursor()
{
  $('body').css('cursor', 'default');
}
function changeToPointerCursor()
{
  $('body').css('cursor', 'pointer');
}
function changeToProgressCursor()
{
  $('body').css('cursor', 'progress');
}

/* End UILogic.js */