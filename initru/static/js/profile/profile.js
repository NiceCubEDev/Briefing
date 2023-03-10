const menuProfileBtn =  [...document.getElementsByName('menu-profile')]
const url = window.location.href 

menuProfileBtn.forEach(btn=>btn.addEventListener('click',()=>{ // события на кнопки
    const namePage = btn.getAttribute('data-name'); // получение названий
    $('#box').load(`${url}${namePage}/`); // в контейнер бокс помещаем данные из ссылки.
}));
// console.log(`${url}detail/`)
// changeData.addEventListener('click', (e)=>{
//     e.preventDefault();
//     $('#box').load(`${url}edit/`);
// });

// myData.addEventListener('click', (e)=>{
//     e.preventDefault();
//     $('#box').load(`${url}detail/`);
// });




