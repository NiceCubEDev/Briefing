console.log('hello')
const url = window.location.href

const quizBox = document.getElementById('quiz-box');

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
                        <input class = "ans" id = '${question}-${answer}' name = '${question}' value = '${answer}' type = 'radio'
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

    
};

quizForm.addEventListener('submit', e => {
    e.preventDefault();
    sendData()
})