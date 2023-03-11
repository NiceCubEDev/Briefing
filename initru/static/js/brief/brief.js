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

modalBtns.forEach(modalBtn=>modalBtn.addEventListener('click', ()=>{
    const briefName = modalBtn.getAttribute('data-brief-name');
    const quizPk = modalBtn.getAttribute('data-quiz-pk');
    const quizName = modalBtn.getAttribute('data-quiz-name');
    const scoreToPass = modalBtn.getAttribute('data-pass');
    const quizTime = modalBtn.getAttribute('data-quiz-time');
    const countQuestions = modalBtn.getAttribute('data-questions');

    modalBody.innerHTML =`
    <div class = 'mb-3'>
        Вы хотите начать тест "<b>${quizName}</b>"?
    </div>
    <div class = 'text-muted'>
        <ul>
            <li>Категория теста: <b>${briefName}</b></li>
            <li>Количество вопросов: <b>${countQuestions}</b></li>
            <li>Для зачёта необходимо: <b>${scoreToPass}%</b></li>
            <li>Время: <b>${quizTime} мин. </b></li>
        </ul>
    </div>
    `;

    const data = {}
    data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    data['quiz'] = quizPk;
    console.log(data)
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
                    window.location.href = url + quizPk;
                }
            },
            error: (response)=>{
                console.log('error');
            }
        });
    });

}));