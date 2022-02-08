// function teste001(idForm, idCampo) {
//     var campo = document.getElementById(idCampo)
//     console.log(campo.value)
// }

if (!$) {
    $ = django.jQuery;
}

// fonte: https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
// $(document).ready(function(){
//   $("#id_nomNro").change(function() {
//     var nomNro = $(this).val();
//     var id_pk_do_modelo = $("#id_pk_do_modelo").val();
//     console.log(nomNro);
//     console.log(id_pk_do_modelo);

//     $.ajax({
//       url: '/ajax/',
//       data: {
//         'nomNro': nomNro,
//         'id_pk_do_modelo': id_pk_do_modelo,
//       },
//       dataType: 'json',
//       success: function (data) {
//         if (data.is_taken) {
//           alert("Número já existe");
//         }
//       }
//     });
//   });
//  });

// TODO: Implementar?
// $(document).ready(function(){
//   $("#documentos_form").submit(function(e) {
    
//     var nomNro = $("#id_nomNro").val();
//     var id_pk_do_modelo = $("#id_pk_do_modelo").val();
//     console.log(nomNro);
//     console.log(id_pk_do_modelo);

//     $.ajax({
//       url: '/ajax/',
//       data: {
//         'nomNro': nomNro,
//         'id_pk_do_modelo': id_pk_do_modelo,
//       },
//       dataType: 'json',
//       async: false,
//       success: function (data) {
//         if (data.is_taken) {
//           if (confirm("Número já existe. Continuar?")) {
//             console.log('sim');
//           } else {
//             e.preventDefault();
//             console.log('não');
//           }
//         }
//       }
//     });
//   });
//   });
