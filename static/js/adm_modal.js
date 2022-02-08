function openModal(fModal, fCampos) {
    let modal = document.getElementById(fModal);
    if (typeof modal == 'undefined' || modal === null)
        return;

    modal.style.display = 'Block';
    document.body.style.overflow = 'hidden';

    let text_span = null;
    let label_value = null;
    if (fCampos != null)
        for (let i = 0; i < fCampos.length; i++) {
            campo = fCampos[i];
            if (campo[0] != "" && campo[1] != "" && typeof campo[0] != 'undefined' && typeof campo[1] != 'undefined' && campo[0] !== null  && campo[1] !== null)
                if (document.getElementById(campo[1]).value == null || document.getElementById(campo[1]).value == "")
                    label_value = campo[0] + ": Não Informado";
                else
                    if (campo[2] == "value")
                        label_value = campo[0] + ": " + document.getElementById(campo[1]).value;
                    else
                        label_value = campo[0] + ": " + document.getElementById(campo[1]).options[document.getElementById(campo[1]).selectedIndex].text;

                if (text_span == null)
                    text_span = label_value ;
                else
                    text_span += '; ' + label_value ;
        }
        if (text_span != null)
            document.getElementById('modal_text_span').innerHTML = text_span;
}

function closeModal(fmodal) {
    let modal = document.getElementById(fmodal);

    if (typeof modal == 'undefined' || modal === null)
        return;

    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}