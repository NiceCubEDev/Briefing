console.log('this is action')

// $('#import-button').click((e)=>{
//     console.log('this is button has clicked');

//     const data={};
//     data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
//     data['download'] = 'true';
//     console.log(data)
//     $.ajax({
//         async: true,
//         type: "POST",
//         url: `${window.location.href}action/`,
//         data:data,
//         success: (response)=>{
//             console.log(response)
//         },
//         error: (response)=>{
//             console.log(response)
//         }
//     });
// });