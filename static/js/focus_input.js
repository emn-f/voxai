// Aguarda o DOM carregar e tenta focar o campo de input do chat
window.addEventListener('DOMContentLoaded', (event) => {
    const chatInputs = window.parent.document.querySelectorAll('textarea');
    if (chatInputs.length > 0) {
        chatInputs[chatInputs.length-1].focus();
    }
});