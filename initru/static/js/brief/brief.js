console.log('hello')

const modalBtns = [...document.getElementsByClassName('btn-quiz')]; // массив с кнопками
const modalBody = document.getElementById('body-form'); // тело модального окна
const url = window.location.href 
const alertContainer = document.getElementById('alertBox');


function notifFunction(type, text) { 
    alertContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
}


function sendData(pk) { // функция проверки 
    const data = {}
    data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    data['quiz'] = pk;
    $('#start-button').unbind('click').click(()=>{
        $.ajax({
            type:"POST",
            url: `${url}check/`,
            data: data,
            success: (response)=>{
                console.log(response)
                if(response.status == false) { 
                    console.log('нет')
                    notifFunction('warning', response.message);
                } else { 
                    window.location.href = url + pk;
                }
            },
            error: (response)=>{
                console.log('error');
            }
        });
    });
}

modalBtns.forEach(modalBtn=>modalBtn.addEventListener('click', ()=>{
    const briefName = modalBtn.getAttribute('data-brief-name');
    const quizPk = modalBtn.getAttribute('data-quiz-pk');
    const quizName = modalBtn.getAttribute('data-quiz-name');
    const scoreToPass = modalBtn.getAttribute('data-pass');
    const quizTime = modalBtn.getAttribute('data-quiz-time');
    const countQuestions = modalBtn.getAttribute('data-questions');
    const linkFile = modalBtn.getAttribute('data-file-link');


    modalBody.innerHTML =`
    <div class = 'mb-3' style = 'font-family: "Roboto-medium";'>
        Вы хотите начать тест "<b>${quizName}</b>"?
    </div>
    <div class = 'text-muted' style = 'font-family: "Roboto-medium";'>
    Характеристика теста: 
        <ul>
            <li>Категория теста: <b>${briefName}</b></li>
            <li>Количество вопросов: <b>${countQuestions}</b></li>
            <li>Для зачёта необходимо: <b>${scoreToPass}%</b></li>
            <li>Время: <b>${quizTime} мин. </b></li>
        </ul>
    </div>
    `;

    if (linkFile != "") {
        modalBody.innerHTML += `
        <div style = 'font-family: "Roboto-medium";'>
            <p>Изучите теорию:</p>
            <a class = 'btn btn-outline-orange' id = 'download-file-link' href = '${linkFile}' download>
                <i class="fa-solid fa-file mx-2"></i>
                Скачать теорию
            </a>
        </div>
        `
    } 

    $('#download-file-link').click(()=>{
        const data = {};
        data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
        data['quiz-pk'] = quizPk;

        $.ajax({
            type:'POST',
            url:`${url}checkFile/`,
            data:data,
            success: (response) => {
                console.log(response);
            },
            error: (response) => {
                console.log(response);
            }
        });
    })

    sendData(quizPk);
}));