date = [...document.getElementsByName('date-start')];
thead = [...document.getElementsByName('filterFunc')];
table = document.getElementById('table');

thead.forEach(elem => elem.addEventListener('click',(e)=>{
    e.preventDefault();

    data = {}

    data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
    data['filter'] = elem.getAttribute('data-name');
    console.log(data)

    $.post(`${window.location.href}passed_brief_filter/`, data, (resp)=>{
        if (resp.status == 'ok') { 
            i = 0
            const tbody = document.createElement("tbody") // создаем боди таблицы
            tbody.style='font-family:"Inter-Regular"'; // стиль
            tbody.setAttribute("id", "id_tbody"); // id 

            console.log(resp)

            result = resp.result
            result.forEach(elem=>{
                i++
                let p = `

                    <tr>
                        <td>${i}</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>

                `

            });

        } else { 
            console.log(resp.status);
        }
    });
}));


   
