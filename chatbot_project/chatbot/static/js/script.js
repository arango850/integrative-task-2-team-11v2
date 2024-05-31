document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', function() {
        const userMessage = userInput.value.trim();
        if (userMessage !== '') {
            sendMessage(userMessage);
            userInput.value = '';
        }
    });

    function sendMessage(message) {
        const userBubble = document.createElement('div');
        userBubble.classList.add('user-bubble');
        userBubble.textContent = message;
        chatBox.appendChild(userBubble);

        // Simula la respuesta del chatbot (aquí puedes llamar a tu función de Python)
        setTimeout(function() {
            const botBubble = document.createElement('div');
            botBubble.classList.add('bot-bubble');
            botBubble.textContent = 'Respuesta del chatbot';
            chatBox.appendChild(botBubble);
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500);
    }
});
