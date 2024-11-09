// sendMessage.js
const fs = require('fs');
const path = require('path');
const express = require('express');
const router = express.Router();

// Function to append a message to the messages.json file
function appendMessageToFile(message, callback) {
  const filePath = path.join(__dirname, 'messages.json');
  
  // Read the current contents of messages.json
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading messages.json:', err);
      return callback(err);
    }
    
    // Parse the file content to get the messages array
    try {
      const messagesArray = JSON.parse(data);
      
      // Append the new message object to the array of messages
      const timestamp = new Date().toISOString();
      const newMessage = { id: messagesArray.length + 1, text: message, timestamp: timestamp };
      messagesArray.push(newMessage);
      
      // Write the updated array back to messages.json
      fs.writeFile(filePath, JSON.stringify(messagesArray, null, 2), 'utf8', (writeErr) => {
        if (writeErr) {
          console.error('Error writing to messages.json:', writeErr);
          return callback(writeErr);
        }
        callback(null, newMessage);
      });
    } catch (parseErr) {
      console.error('Error parsing messages.json:', parseErr);
      callback(parseErr);
    }
  });
}

// Express route setup for POST request to send messages
router.post('/send', (req, res) => {
  const message = req.body.message;
  if (typeof message !== 'string' || message.trim() === '') {
    return res.status(400).json({ error: 'Message must be a non-empty string.' });
  }
  
  appendMessageToFile(message, (err, newMessage) => {
    if (err) {
      return res.status(500).json({ error: 'Server error occurred.' });
    }
    res.status(200).json(newMessage);
  });
});

module.exports = router;
