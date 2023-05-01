const passBtn = document.getElementById('pass_query') // кнопка отправки
const alertContainer = document.getElementById('alertBox');
const url = 'sendMessage/';
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

function notifFunction(type, text) { 
    alertContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
}


$('#contact-form').submit((e)=>{
    e.preventDefault();

    const myData = {}
    myData['csrfmiddlewaretoken'] = csrf
    myData['name_contact'] = $("#id_name_contact").val();
    myData['email_contact'] = $("#id_email_contact").val();
    myData['text_contact'] =  $("#id_text_contact").val();


    $.ajax({
        type:'POST',
        url: url,
        data: myData,
        success: (resp)=>{
            if(resp.status == 'ok') { 
                notifFunction('success', resp.message)
            } else { 
                notifFunction('danger', resp.message)
            }
        },
        error: (resp)=>{
            console.log(resp);
        }
    })
});



