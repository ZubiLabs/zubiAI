// receiveMessage.js
const fs = require('fs');
const path = require('path');

function getMessages(req, res) {
  const messagesFilePath = path.join(__dirname, 'messages.json');
  fs.readFile(messagesFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading messages.json:', err);
      return res.status(500).json({ error: 'Internal server error' });
    }
    try {
      const messages = JSON.parse(data);
      res.status(200).json(messages);
    } catch (parseErr) {
      console.error('Error parsing messages.json:', parseErr);
      res.status(500).json({ error: 'Internal server error' });
    }
  });
}

function setupReceiveMessagesEndpoint(app) {
  app.get('/api/messages/receive', getMessages);
}

module.exports = setupReceiveMessagesEndpoint;
