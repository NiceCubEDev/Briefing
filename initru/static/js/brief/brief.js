console.log('hello')

const modalBtns = [...document.getElementsByClassName('btn-quiz')]; // массив с кнопками
const modalBody = document.getElementById('body-form'); // тело модального окна
const startBtn = document.getElementById('start-button');

modalBtns.forEach(modalBtn=>modalBtn.addEventListener('click', ()=>{
    const briefPk = modalBtn.getAttribute('data-brief-pk');
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
    `
}));