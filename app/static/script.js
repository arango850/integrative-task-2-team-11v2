document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const clearButton = document.getElementById("clear-button");

    function showMessageUser(message) {
        const userMessage = document.createElement("p");
        userMessage.textContent = "Usuario: " + message;
        chatBox.appendChild(userMessage);
    }
 
    function showMessageChatbot(message) {
        const chatbotMessage = document.createElement("p");
        chatbotMessage.textContent = "Chatbot: " + message;
        chatBox.appendChild(chatbotMessage);
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (message !== "") {
            showMessageUser(message);
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                showMessageChatbot(data.response);
                
                if (data.explanation) {
                    showMessageChatbot(data.explanation);
                    showMessageChatbot("¿Te gustaría saber más sobre esta emoción?");
                }
            })
            .catch(error => console.error('Error:', error));
            userInput.value = ""; // Limpiar el campo de entrada
        }
    }
    
    function expandInfo() {
        const userResponse = "sí"; // Cambiar esto si lo necesitas
        fetch('/expand', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userResponse })
        })
        .then(response => response.json())
        .then(data => showMessageChatbot(data.response))
        .catch(error => console.error('Error:', error));
    }
    

    sendButton.addEventListener("click", sendMessage);

    clearButton.addEventListener("click", function() {
        chatBox.innerHTML = ""; // Limpiar el historial de mensajes
        userInput.value = ""; // Limpiar el campo de entrada
    });

});



