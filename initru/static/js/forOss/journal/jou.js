
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
 

    $.ajax({
        type:"POST",
        url: window.location.href,
        data: dataFilter,
        success:(resp)=>{
            console.log(resp);
        },
        errors:(resp)=>{
            console.log(resp);
        },
    });

})