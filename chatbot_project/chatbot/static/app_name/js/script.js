document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Función para enviar mensaje cuando se presiona Enter
    userInput.addEventListener('keyup', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            sendBtn.click();
        }
    });

    // Función para enviar mensaje cuando se hace clic en el botón
    sendBtn.addEventListener('click', function() {
        const userMessage = userInput.value.trim();
        if (userMessage !== '') {
            sendMessage(userMessage, 'user');
            // Lógica del chatbot aquí para generar una respuesta
            // Ejemplo de respuesta del chatbot
            const botResponse = '¡Hola! Soy un chatbot. ¿En qué puedo ayudarte?';
            sendMessage(botResponse, 'bot');
            userInput.value = '';
        }
    });

    // Función para agregar un mensaje al chat
    function sendMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.innerText = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
