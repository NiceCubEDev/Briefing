const data = {}
const box = document.createElement("p")
$('#bot-form').submit((e)=>{
    e.preventDefault();
    data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
    data['message'] = $('input[name="message"]').val();
    $.ajax({
        type:"POST",
        url: window.location.href,
        data: data,
        success: (resp)=>{
            box.innerHTML += resp.response
            $('#response-box').append(box)
        },
        error: ()=>{
            console.log(response);
        },
    });
});