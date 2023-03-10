const changeBtn = [...document.getElementsByName('change-data')];
const csrf = document.getElementsByName('csrfmiddlewaretoken')

changeBtn.forEach(btn=>btn.addEventListener('click', ()=>{
    const btnType = btn.getAttribute('data-type');
    const btnValue = btn.getAttribute('data-content');
    console.log(btnValue);
    console.log(csrf[0].value);
}));