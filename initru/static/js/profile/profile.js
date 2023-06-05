const menuProfileBtn =  [...document.getElementsByName('menu-profile')]
const url = window.location.href // получение ссылки страницы

menuProfileBtn.forEach(btn=>btn.addEventListener('click',()=>{ // события на кнопки
    const namePage = btn.getAttribute('data-name'); // получение названий
    $('#box').load(`${url}${namePage}/`); // в контейнер бокс помещаем данные из ссылки.
}));






