date = [...document.getElementsByName('date-start')];
thead = [...document.getElementsByName('filterFunc')];
table = document.getElementById('table');
mark = null;


thead.forEach(elem => elem.addEventListener('click',(e)=>{

    e.preventDefault();
    data = {}
    data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();

    if (elem.getAttribute('data-name').includes("-")) { // если есть минус, то 
        elem.setAttribute('data-name',`${elem.getAttribute('data-name').replace('-','')}`); // меняем значение и вырезаем минус
        data['filter'] = elem.getAttribute('data-name'); // берём значение
    } else { 
        elem.setAttribute('data-name',`-${elem.getAttribute('data-name')}`); // Если нет минуса, то добавляем минус
        data['filter'] = elem.getAttribute('data-name'); // записываем
    }

    $.post(`${window.location.href}passed_brief_filter/`, data, (resp)=>{
        if (resp.status == 'ok') { 

            i = 0
            const tbody = document.createElement("tbody") // создаем боди таблицы
            tbody.style='font-family:"Inter-Regular"'; // стиль
            tbody.setAttribute("id", "id_tbody"); // id 
            result = resp.result
            
            result.forEach(elem=>{

                let date = new Date(elem.date_start) // переводим в нормальное время
                i++

                if(elem.mark == 'Сдан') {
                    mark = `
                        <td class = 'text-center text-light bg-success bg'>
                            ${elem.mark}
                        </td>
                    `;
                } else { 
                    mark = `
                        <td class = 'text-center text-light bg-danger'>
                            ${elem.mark}
                        </td>
                    `;
                }

                let p = `

                    <tr>
                        <td>${i}</td>
                        <td>${elem.name_brief}</td>
                        <td style = 'max-width: 375px;'>${elem.quiz_name}</td>
                        <td>${date.toLocaleString()}</td>
                        <td class = 'text-center'>${elem.result}%</td>
                        ${mark}
                    </tr>

                `
                tbody.innerHTML += p
            });
            $('#id_tbody').remove(); // удаляем старое тело
            table.appendChild(tbody) // добавляем новое тело

        } else { 
            console.log(resp.status);
        }
    });
}));


   
