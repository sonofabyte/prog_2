//alert("im alive");

function delNote(id) {
  $.ajax({
    url: "/api/delNote",
    method: "POST",
    data: { item_id: id },
  }).done(function(response) {
    console.log(response);
    location.reload();

  }).fail(function( jqXHR, textStatus ) {
    alert("fail");
  });
}

var exampleModal = document.getElementById('newNote')

//configure modal content on open
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
      title_edit.value = "";
      text_edit.value = "";
    }

    idField.value = itemN;

})