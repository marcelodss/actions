if (!$) {
  $ = django.jQuery;
}

function myFunction() {
    if (!confirm('Confirma envio?')) {
      console.log("NÃO ENVIADO")
      return false;
    } 
    else {
      console.log("ENVIADO")
      return true;
    }
  }

function newFunction() {
  $(function () {
      $("#dom").text("O DOM agora está carregado e pode ser manipulado.");
  });
}

function confirmSubmit() {
  var yes=confirm("Tem certeza que deseja continuar?");
  if (yes)
    return true;
  else
    return false;
}


$(document).ready(function(){
  $('form').submit(function() {
    // if (confirm('confirma Envio?')) {

      this.submit();
      // $("#add_movie").addClass('desabilita');
      
      $('#container').append('<div class="overlay_div"></div>');
      $(".overlay_div").wrap('<div class="overlay_text">A g u a r d e . . .</div>');
      $('.overlay_div').append('<div class="loader"></div>');
      $(".wait_wrap").hide();
      $(".submit-row").addClass('submit-row_off');
      $(".wait_off").addClass('wait_on');
      // $(".wait_off").text('Aguarde um tantinho...');
      $(".wait_off").append('<i class="fa fa-spinner fa-spin"></i> Aguarde um tantinho...');

    // }
});
});
