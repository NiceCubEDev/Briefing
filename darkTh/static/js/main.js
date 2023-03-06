blockError = document.getElementById("message-block")
stick = document.getElementById('message-close')

function closeErrorBlock() {
    blockError.style.display = 'none';
}

stick.addEventListener('click', closeErrorBlock)

