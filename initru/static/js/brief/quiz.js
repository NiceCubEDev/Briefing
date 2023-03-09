console.log('hello')
const url = window.location.href

const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box')


console.log()
$.ajax({
    type: 'GET',
    url:`${url}/data`,
    success:(res)=>{
        console.log(res)
        const data = res.data
        data.forEach(el=>{
            for (const [question, answers] of Object.entries(el)) {
                quizBox.innerHTML += `
                <div class = 'mb-2 mt-4'>
                    <b>${question}</b>
                </div>
                `;
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                    <div class = ''>
                        <input class = "ans" id = '${question}-${answer}' name = '${question}' value = '${answer}' type = 'radio'/>
                        <label for = "${question}">${answer} </label>
                    </div>
                    `;
                });
            };
        });
    },
    errors:(res)=>{
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
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]){
                data[el.name] = null;
            }
        }
    });

    console.log(data)

    $.ajax({
        type:'POST',
        url:`${url}/save`,
        data: data,
        success: (res)=>{
            const results = res.results
            console.log(results)
            quizForm.remove(); // удаление формы
            
            scoreBox.innerHTML = `<p class = 'fs-5'> ${res.passed ? '<b>Вы сдали!</b>' : '<b>Вы не сдали!</b>'} Ваш результат: <b>${res.score}%</b> </p>`;
            

            results.forEach(res=>{
                const resDiv = document.createElement("div");
                for (const [question, resp] of Object.entries(res)){
                    // console.log(question)
                    // console.log(resp)
                };
            })

        },
        error: (res)=>{
            console.log(res)
        }
    })
};

quizForm.addEventListener('submit', e => {
    e.preventDefault();
    sendData()
})