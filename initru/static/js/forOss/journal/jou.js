// const table = document.getElementById;
// console.log(table);


$('#filter-form').submit((e)=>{
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
            i=0

            // const tbody = document.createElement("tbody")

            resp.result.forEach(elem => {
                let date = new Date(elem.date_start)
                let date2 = new Date(elem.date_end)
                i++

                // let p = `
                // <tr>
                //     <td>${i}</td>
                //     <td>${elem.surname}</td>
                //     <td>${elem.name}</td>
                //     <td>${elem.patro}</td>
                //     <td>${elem.group}</td>
                //     <td>${elem.type_user}</td>
                //     <td>${elem.type_user_test}</td>
                //     <td>${elem.brief}</td>
                //     <td>${elem.quiz_name}</td>
                //     <td>${date.toLocaleString()}</td>
                //     <td class = 'text-center'>${date2.toLocaleDateString()}</td>
                //     <td class = 'text-center'>${elem.score} %</td>
                //     <td class = 'text-center'>${elem.mark}</td>
                // </tr>
                // `
                // tbody.appendChild(p)
                $('#id_tbody').html($(`
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
                        <td class = 'text-center'>${date2.toLocaleDateString()}</td>
                        <td class = 'text-center'>${elem.score} %</td>
                        <td class = 'text-center'>${elem.mark}</td>
                    </tr>
                `))
            });
            
        },
        errors:(resp)=>{
            console.log(resp);
        },
    });

})