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
            <input class = 'form-control' autocomplete="off" type = '${type}' name = '${name}' id = 'id_${name}' placeholder = 'Введите новый номер телефона' /> <br/>
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
            <i class="fa-regular fa-face-grin-hearts mx-3 text-success"></i>
            <input class = 'form-control' autocomplete="off" type = '${type}' name = '${name}' id = 'id_${name}'/> <br/>
        </div>
        <div class = 'd-flex align-items-center'>
            <i class="fa-solid fa-key mx-3 text-primary"></i>
            ${passwordContent}
        </div> 
        `
    }

    if (name == 'password') {
        formBody.innerHTML = `
        <div class = 'd-flex align-items-center mb-2'>
        <i class="fa-solid fa-key mx-3 text-primary text-danger"></i>
            <input class = 'form-control' autocomplete="off" type = '${type}' name = '${name}' id = 'id_${name}' placeholder = 'Введите старый пароль' /> <br/>
        </div>
        <div class = 'd-flex align-items-center mb-2'>
            <i class="fa-solid fa-key mx-3 text-primary text-success"></i>
            <input class = 'form-control' autocomplete="off" type = 'password' name = 'password1' id = 'id_password1' placeholder = 'Введите новый пароль' />
        </div> 
        <div class = 'd-flex align-items-center mb-2'>
            <i class="fa-solid fa-key mx-3 text-primary text-success"></i>
            <input class = 'form-control' autocomplete="off" type = 'password' name = 'password2'  id = 'id_password2' placeholder = 'Повторите новый пароль' />
        </div> 
        <p class = 'text-center'>Новый пароль должен быть не менее <span class = 'text-danger'>8 символов</span>!</p>

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
        
        const datas = new FormData() // константа для отправки

        if (input[0].name == 'avatar') { 
            datas.append('csrfmiddlewaretoken', csrf[0].value)
            datas.append([`${input[0].name}`], input[0].files[0])
            datas.append('password', passwordInput.value)
        } 
        if (input[0].name == 'password'){

            const password1 = document.getElementsByName('password1')
            const password2 = document.getElementsByName('password2')

            datas.append('csrfmiddlewaretoken', csrf[0].value)
            datas.append([`${input[0].name}`], input[0].value)
            datas.append('password', passwordInput.value)
            datas.append('password1', password1[0].value)
            datas.append('password2', password2[0].value)
        }
        else { 
            datas.append('csrfmiddlewaretoken', csrf[0].value)
            datas.append([`${input[0].name}`], input[0].value)
            datas.append('password', passwordInput.value)
        }
        
        $.ajax({
            async:true,
            type: "POST",
            url: `${url}change/`,
            enctype:'multipart/form-data',
            data: datas,
            success: (response)=> {
                console.log(response.phone_number)
                stat = response.status
                if (stat == 'ok') {
                    notifFunction('success', response.message)
                    if (response.reload == 'go') {
                        setInterval(()=>{
                            $(location).prop('href','/'); // Перекидываем на главную, если сменили пароль
                        }, 2500);
                    }
                } else { 
                    notifFunction('danger', response.message)
                }
            },
            error: (response)=> {
                console.log(response);
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    });
}));


