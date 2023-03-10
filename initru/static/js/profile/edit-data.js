changeBtn = [...document.getElementsByName('change-data')];
formBody = document.getElementById('change-form');



changeFunction = (type, name) => {
    const passwordContent = `
    <input class = 'form-control' type = 'password' autocomplete="off" name = 'password' id='id_password' placeholder = 'Подтвердите паролем' />
    `;

    if (name == 'email') {
        formBody.innerHTML = `
        <div class = 'd-flex align-items-center mb-2'>
            <i class="fa-solid fa-square-envelope mx-3" style='color:#E7882B;'></i>
            <input class = 'form-control' type = '${type}' name = '${name}' id = 'id_${name}' placeholder = 'Введите новую почту' /> <br/>
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
            <input class = 'form-control' type = '${type}' name = '${name}' '${name}' id = 'id_${name}' placeholder = 'Введите новый номер телефона' /> <br/>
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


    $('#start-button').unbind('click').click((e)=>{ // unbind чтобы убрать отправку, которая дублируется 
        e.preventDefault();
        const input = document.getElementsByName(name); // получение данных 
        const passwordInput = document.getElementById('id_password'); // получение данных 
        const url = window.location.href; // получение ссылк на профиль
        const csrf = document.getElementsByName('csrfmiddlewaretoken');
        
        $.ajax({
            type: "POST",
            url: url,
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                [`${input[0].name}`]: input[0].value,
                'password':passwordInput.value,
            },
            success: (response)=> {
                console.log('good');
            },
            error: (response)=> {
                console.log('error');
            }
        });
    });
}));


