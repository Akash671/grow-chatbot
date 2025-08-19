document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const sendMessage = async () => {
        const query = userInput.value.trim();
        if (query === '') return;

        // Display user message
        appendMessage(query, 'user-message');
        userInput.value = '';
        
        // Show typing indicator
        // Corrected line: 'bot-message' and 'typing-indicator' are now separate arguments
        const typingIndicator = appendMessage('Typing...', 'bot-message', 'typing-indicator');
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            // Send message to the backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: query }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Remove typing indicator and show bot response
            typingIndicator.remove();
            appendMessage(data.response, 'bot-message');

        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            appendMessage("Sorry, I'm having some trouble connecting. Please try again.", 'bot-message');
        }
    };

    const appendMessage = (text, ...classNames) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', ...classNames);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageElement;
    };
    
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});