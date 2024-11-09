// server.js
const express = require('express');
const setupReceiveMessagesEndpoint = require('./receiveMessage');
const sendMessageEndpoint = require('./sendMessage');
const path = require('path');
const app = express();

// Middleware to parse JSON bodies
app.use(express.json());

// Serve static files from the root directory
app.use(express.static(path.join(__dirname)));

// Setup send and receive messages endpoints
app.use('/api/messages', sendMessageEndpoint);
setupReceiveMessagesEndpoint(app);

// Use environment variable for port or default to 3000
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is up and running on port ${port}`);
});
