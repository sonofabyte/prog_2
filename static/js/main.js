/**
 * 
 * delete note from database
 * 
 * send a POST request to server with the note ID to be deleted
 * 
 * with help from stack overflow
 */
function delNote(id) {
  $.ajax({
    url: "/api/delNote",
    method: "POST",
    data: { item_id: id },
  }).done(function(response) {
    console.log(response);
    location.reload();

  }).fail(function( jqXHR, textStatus ) {
    //Request was unsuccessful
    alert("Failed deleting note.");
  });
}

// get a reference to the note edit modal
var exampleModal = document.getElementById('newNote')

/**
 * configure modal content on open
 *
 * request note to edit as JSON from server
 * set text of form in modal from JSON 
 * 
 * mostly taken from getbootstrap
 */
exampleModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var itemN = 0;
    var title_edit = exampleModal.querySelector('#titleedit');
    var text_edit = exampleModal.querySelector('#textedit');
    var idField = exampleModal.querySelector('#idField');

    if (button.getAttribute('data-bs-edit') == "true"){
        itemN = button.getAttribute('data-bs-item');
        $.ajax({
            url: "/api/modNote",
            method: "POST",
            data: { item_id: itemN, process: "get"},
          }).done(function(response) {
            console.log(response);
            title_edit.value = response.title;
            text_edit.value = response.content;
    
          }).fail(function( jqXHR, textStatus ) {
            alert("fail");
          });
    }
    else{
      // no note to edit -> reset form to be empty
      title_edit.value = "";
      text_edit.value = "";
    }

    //set invisible field to note ID
    idField.value = itemN;

})