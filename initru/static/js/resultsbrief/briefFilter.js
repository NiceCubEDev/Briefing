const date = [...document.getElementsByName('date-start')];
const thead =[...document.getElementsByName('filterFunc')];


thead.forEach(elem => elem.addEventListener('click',(e)=>{
    e.preventDefault();

    const data = {}

    data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
    // data[`${elem.getAttribute('name')}`] = elem.getAttribute('data-name');
    data['filter'] = elem.getAttribute('data-name');
    console.log(data)

    $.post(`${window.location.href}passed_brief_filter/`, data, (resp)=>{
        console.log(resp);
    });
}));


   
