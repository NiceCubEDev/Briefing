const table = document.getElementById('table');
let mark;
alertContainer = document.getElementById('alertBox');


function notifFunction(type, text) { 
    alertContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        <strong>${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
}

$('#setBut').click((e)=>{
    e.preventDefault();

    const dataFilter = {}
    dataFilter['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
    dataFilter['id_type_user'] = $('#id_type_user').val();
    dataFilter['id_brief'] = $('#id_type_brief').val();
    dataFilter['id_group'] = $('#id_group').val();
    dataFilter['id_quiz'] = $('#id_quiz').val();
    dataFilter['id_date_start'] = $('#id_date_start').val();
    dataFilter['id_date_end'] = $('#id_date_end').val();
    dataFilter['mark'] = $('#id_mark').val();

    $.ajax({
        type:"POST",
        url: window.location.href,
        data: dataFilter,
        success:(resp)=>{
            console.log(resp)
            if (Boolean(resp.result)) { 
                i=0 // счетчик

                
    
                const tbody = document.createElement("tbody") // создаем боди таблицы
                tbody.style='font-family:"Inter-Regular"'; // стиль
                tbody.setAttribute("id", "id_tbody"); // id 
                
                resp.result.forEach(elem => { // проходимся по результатам
                    
                    let date = new Date(elem.date_target)
                    let date1 = new Date(elem.date_passed)
                    i++

                    
                    if(elem.mark == 'Сдан') {
                        mark = `
                            <span class = 'text-center text-success'>
                                ${elem.mark}
                            </span>
                        `;
                    } else { 
                        mark = `
                            <span class = 'text-center text-danger'>
                                ${elem.mark}
                            </span>
                        `;
                    }
    
            
                    let p = `
                    <tr>
                        <td>${i}</td>
                        <td>${elem.surname}</td>
                        <td>${elem.name}</td>
                        <td>${elem.patro}</td>
                        <td>${elem.group}</td>
                        <td>${elem.type_user}</td>
                        <td>${elem.type_user_test}</td>
                        <td>${elem.brief}</td>
                        <td>${elem.quiz_name}</td>
                        <td>${date.toLocaleString()}</td>
                        <td>${date1.toLocaleString()}</td>
                        <td class = 'text-center'>${elem.days_skiped} дней</td>
                        <td class="text-center">
                            <button class = 'btn btn-outline-orange'>
                                <i class="fa-solid fa-envelope mx-2"></i>
                                Отправить
                            </button>
                        </td>
                        <td class = 'text-center'>${elem.score} %</td>
                        <td>${mark}</td>
                    </tr>
                    `
                    tbody.innerHTML += p
                });
                $('#id_tbody').remove(); // удаляем боди таблицы
                table.appendChild(tbody);
                notifFunction('success', resp.message);
            } else {
                notifFunction('danger', resp.message);
            }

        },
        errors:(resp)=>{
            console.log(resp);
        },
    });

});
