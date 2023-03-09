const url = window.location.href

const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box');
const timerBox = document.getElementById('timerParag');
const alertContainer = document.getElementById('alertBox');

function notifFunction(type, text) { 
    alertContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
}


const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `0${time}:00`;
    } else {
        timerBox.innerHTML = `${time}:00`;
    }

    let minutes = time - 1;
    let seconds = 60;
    let displaySeconds;
    let displayMinutes;

    const timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59;
            minutes--
        };
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes;
        } else {
            displayMinutes = minutes;
        };
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds;
        } else { 
            displaySeconds = seconds
        };
        if (minutes === 0 && seconds === 0) { 
            timerBox.innerHTML = '00:00';
            setTimeout(() => {
                clearInterval(timer);
                notifFunction('success', 'Конец теста.');
                sendData();
            }, 500);
        }
        timerBox.innerHTML = `${displayMinutes}:${displaySeconds}`;
    }, 1000);
};


$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: (res) => {
        console.log(res)
        const data = res.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                quizBox.innerHTML += `
                <div class = 'mb-2 mt-3'>
                    <b>${question}</b>
                </div>
                `;
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                    <div>
                        <input class = "ans" id = '${question}-${answer}' name = '${question}' value = '${answer}' type = 'radio'/>
                        <label for = "${question}">${answer} </label>
                    </div>
                    `;
                });
            };
        });
        activateTimer(res.time)
    },
    errors: (res) => {
        console.log(res)
    },
});


const quizForm = document.getElementById('quiz-form'); // взяли форму с тестами
const csrf = document.getElementsByName('csrfmiddlewaretoken'); // взяли токен 

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]; // получили варианты 
    // console.log(elements)

    const data = {}

    data['csrfmiddlewaretoken'] = csrf[0].value;
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null;
            }
        }
    });

    console.log(data)

    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: (res) => {
            const results = res.results
            console.log(res)
            quizForm.remove(); // удаление формы

            scoreBox.innerHTML = `Итог: ${res.passed ? '<b class = "text-success">Вы сдали!</b>' : '<b class = "text-danger">Вы не сдали!</b>'} <br/> Ваш результат: <b>${res.score.toFixed(2)}%</b> <br/> Количество верных ответов: ${res.countAnswers} шт.`;


            results.forEach(res => {
                const resDiv = document.createElement("div");
                for (const [question, resp] of Object.entries(res)) {
                    // console.log(question)
                    // console.log(resp)

                    resDiv.innerHTML += `<b>${question}</b>` + '<br/>' // добавление вопросов в див
                    const cls = ['container', 'p-3', 'text-white', 'mt-2'] // классы для див
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered') {  // если ответ пустой
                        resDiv.innerHTML += '- нет ответа';
                        resDiv.classList.add('bg-danger');
                    } else {
                        const answer = resp['answered']; // ответ пользователя
                        const correct = resp['correct_answer'] // ответ из бд

                        if (answer == correct) {
                            resDiv.classList.add('bg-success');
                            resDiv.innerHTML += `Ваш ответ: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger');
                            resDiv.innerHTML += `Правильный ответ: ${correct} <br/>`;
                            resDiv.innerHTML += `Ваш ответ: ${answer}`;
                        };
                    };

                };
                resultBox.append(resDiv)
            })

        },
        error: (res) => {
            console.log(res)
        }
    })
};

quizForm.addEventListener('submit', e => {
    e.preventDefault();
    notifFunction('success', 'Конец теста.');
    sendData()
})