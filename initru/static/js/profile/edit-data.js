changeBtn = [...document.getElementsByName('change-data')];
formBody = document.getElementById('change-form');
alertContainer = document.getElementById('alertBox');


function notifFunction(type, text) { 
    alertContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
}


changeFunction = (type, name) => {
    const passwordContent = `
    <input class = 'form-control' type = 'password' autocomplete="off" name = 'password' id='id_password' placeholder = 'Подтвердите паролем' />
    `;

    if (name == 'email') {
        formBody.innerHTML = `
        <div class = 'd-flex align-items-center mb-2'>
            <i class="fa-solid fa-square-envelope mx-3" style='color:#E7882B;'></i>
            <input class = 'form-control' autocomplete="off" type = '${type}' name = '${name}' id = 'id_${name}' placeholder = 'Введите новую почту' /> <br/>
        </div>
        <div class = 'd-flex align-items-center'>
            <i class="fa-solid fa-key mx-3 text-primary"></i>
            ${passwordContent}
        </div> 
        `
    }

    if (name == 'phone_number') {
        formBody.innerHTML = `
        <div class = 'd-flex align-items-center mb-2'>
            <i class="fa-solid fa-hashtag mx-3" style='color:#E7882B;'></i>
            <input class = 'form-control' autocomplete="off" type = '${type}' name = '${name}' '${name}' id = 'id_${name}' placeholder = 'Введите новый номер телефона' /> <br/>
        </div>
        <div class = 'd-flex align-items-center'>
            <i class="fa-solid fa-key mx-3 text-primary"></i>
            ${passwordContent}
        </div> 
        `
    }

    if (name == 'avatar') {
        formBody.innerHTML = `
        <div class = 'd-flex align-items-center mb-2'>
            <i class="fa-regular fa-face-grin-hearts mx-3" style='color:#E7882B;'></i>
            <input class = 'form-control' autocomplete="off" type = '${type}' name = '${name}' '${name}' id = 'id_${name}'/> <br/>
        </div>
        <div class = 'd-flex align-items-center'>
            <i class="fa-solid fa-key mx-3 text-primary"></i>
            ${passwordContent}
        </div> 
        `
    }



}

changeBtn.forEach(btn => btn.addEventListener('click', () => { // делаем событие для всех кнопок
    const btnType = btn.getAttribute('data-type');  // берём нужные данные
    const btnName = btn.getAttribute('data-type-name'); // берём нужные данные

    changeFunction(btnType, btnName); // в функцию 


    $('#start-button').unbind('click').click((e)=>{ // unbind чтобы убрать отправку,
        e.preventDefault();
        
        const input = document.getElementsByName(btnName); // получение данных 
        const passwordInput = document.getElementById('id_password'); // получение данных 
        const url = window.location.href; // получение ссылк на профиль
        const csrf = document.getElementsByName('csrfmiddlewaretoken');
        $.ajax({
            type: "POST",
            url: url,
            enctype:'multipart/form-data',
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                [`${input[0].name}`]: input[0].value,
                'password':passwordInput.value,
            },
            success: (response)=> {
                stat = response.status
                if (stat == 'ok') {
                    notifFunction('success', response.message)
                } else { 
                    notifFunction('danger', response.message)
                }
            },
            error: (response)=> {
                console.log(response);
            },

        });
    });
}));


