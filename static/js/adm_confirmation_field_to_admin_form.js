//  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
//  - Utilizado para setar o valor do campo 'id_confirmation_field' para 'False';
// 
//  - A ação ocorrerá se encontrar o atributo 'reconfirm_flag' igual a 'yes' que foi criado 
//  na def __init__, da classe 'ConfirmFieldToAdminForm' no arquivo 
//  'mixins\confirmation_field_to_admin_form.py', garantindo que o campo 'id_confirmation_field' 
//  seja recarregado mesmo após já ter sido utilizado e ocorrerem alterações efetuadas pelos 
//  usuários em outros campos antes de um submit, com ou sem a ocorrência das inconsistências 
//  detectadas pelas validações do Django.
//  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

if (!$) {
    $ = django.jQuery;
  }

// alert('teste')
console.log('chegou!!!')


$(document).ready(function() {
	
	//CSS selectors
	var valor = $('#id_confirmation_field').val();
	console.log(valor);
    var reconfirm_flag = $("#id_confirmation_field").attr("reconfirm_flag");

    if (reconfirm_flag=='yes') {
        $('#id_confirmation_field').val(false);
    }

    console.log(reconfirm_flag)

	// //DOM traversing (more efficient)
	// result = $('#animals').find('.creature');
	// console.log(result);
});