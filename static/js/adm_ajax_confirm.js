if (!$) {
    $ = django.jQuery;
  }

$(document).ready(function(){
    $("form").submit(function(e) {

      var formData = $('form').serializeArray();
      formData = objectifyForm(formData);
      console.log(formData);
      console.log(typeof(formData));

      $.ajax({
        url: '/ajax/teste/',
        data: formData,
        dataType: 'json',
        async: false,
        success: function (data) {
          if (data.erro != 'N') {
            if (confirm(data.erro)) {
              console.log('sim');
            } else {
              e.preventDefault();
              console.log('não');
            }
          }
        }
      });
    });
});



// VER: Serialização
// https://stackoverflow.com/questions/44481546/how-to-send-json-serialize-data-from-a-form-to-ajax-using-django 

function mySerialize(pk_model = 0) {
var formData = $('form').serializeArray();
formData = objectifyForm(formData);
formData["pk_model"] = pk_model;
console.log(formData);
console.log(typeof(formData));

$.ajax({
    url: '/ajax/teste/',
    data: formData,
    dataType: 'json',
    // async: false,
    success: function(data) {
    if (data.erro == 'N'){
        console.log('sem erro');
    } else {
        console.log(data.erro);
    }
    },
});
}

function objectifyForm(formArray) {
    var returnArray = {};
    for (var i=0;i<formArray.length;i++) {
        if (formArray[i].value) {
            returnArray[formArray[i].name] = formArray[i].value;
        }
    }
    return returnArray;
}
