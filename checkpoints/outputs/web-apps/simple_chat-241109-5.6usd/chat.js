// chat.js
document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const chatContainer = document.getElementById('chat-container');

    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = ''; // Clear the input after sending
        }
    });

    // Add event listener for "Enter" key
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const message = messageInput.value.trim();
            if (message) {
                sendMessage(message);
                messageInput.value = ''; // Clear the input after sending
            }
        }
    });

    // Initialize polling for messages
    setInterval(receiveMessages, 2000);
});

function sendMessage(message) {
    fetch('/api/messages/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message === 'Message sent successfully.') {
            // Update the UI with the sent message
            updateChatContainer([{ text: message, timestamp: new Date().toISOString() }]);
        }
    })
    .catch(error => console.error('Error sending message:', error));
}

function receiveMessages() {
    fetch('/api/messages/receive')
        .then(response => response.json())
        .then(messages => {
            if (messages.length > 0) {
                updateChatContainer(messages);
            }
        })
        .catch(error => console.error('Error receiving messages:', error));
}

function updateChatContainer(messages) {
    messages.forEach(msg => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.textContent = msg.text;
        // Determine if the message was sent or received
        if (msg.timestamp > lastMessageTimestamp) {
            messageElement.classList.add('received');
        } else {
            messageElement.classList.add('sent');
        }
        chatContainer.appendChild(messageElement);
    });
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom
    // Update last message timestamp
    lastMessageTimestamp = messages[messages.length - 1].timestamp;
}

// Keep track of the last message timestamp to avoid duplicates
let lastMessageTimestamp = '1970-01-01T00:00:00.000Z';
