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