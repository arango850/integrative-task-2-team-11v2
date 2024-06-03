document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const clearButton = document.getElementById("clear-button");

    // Función para mostrar mensajes del usuario en el chat
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

    // Evento click del botón "Enviar"
    sendButton.addEventListener("click", function() {
        const message = userInput.value.trim();
        if (message !== "") {
            showMessageUser(message);
            // Aquí puedes llamar a una función que procese la entrada del usuario y genere la respuesta del chatbot
            // Por ahora, simplemente simularemos una respuesta del chatbot
            showMessageChatbot("¡Hola! Soy el chatbot de salud mental. ¿En qué puedo ayudarte?");
            userInput.value = ""; // Limpiar el campo de entrada
        }
    });

    // Evento click del botón "Nuevo chat"
    clearButton.addEventListener("click", function() {
        chatBox.innerHTML = ""; // Limpiar el historial de mensajes
        userInput.value = ""; // Limpiar el campo de entrada
    });
});
