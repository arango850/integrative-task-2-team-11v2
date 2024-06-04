document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const clearButton = document.getElementById("clear-button");

    function showMessageUser(message) {
        const userMessage = document.createElement("p");
        userMessage.textContent = "User: " + message;
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
                    showMessageChatbot("Would you like to know more about this emotion?");
                }
            })
            .catch(error => console.error('Error:', error));
            userInput.value = ""; // Clear the input field
        }
    }
    
    function expandInfo() {
        const userResponse = "yes"; // Change this if needed
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
        chatBox.innerHTML = ""; // Clear chat history
        userInput.value = ""; // Clear the input field
    });

});




