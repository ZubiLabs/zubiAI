# README.md
# Simple Web Chat Interface

## Introduction
This application provides a minimalistic web-based chat interface for personal use, allowing users to send and receive plain text messages.

## Setup Instructions

### Prerequisites
- Node.js installed on your system.
- Docker installed if you wish to run the application within a Docker container.

### Installation Steps
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run `npm install` to install the dependencies.

## Running the Application

### Locally
1. Start the server with `npm start`.
2. Open your web browser and navigate to `http://localhost:3000`.

### Within Docker
1. Build the Docker image with `docker build -t simple-web-chat-interface .`.
2. Run the Docker container with `docker run -p 3000:3000 simple-web-chat-interface`.
3. Open your web browser and navigate to `http://localhost:3000`.

## API Endpoints

### Send Message
- **POST** `/api/messages/send`
  - **Request Body**: `{ "message": "Your message here" }`
  - **Response**: `{ "message": "Message sent successfully.", "timestamp": "2023-01-01T00:00:00.000Z" }`

### Receive Messages
- **GET** `/api/messages/receive`
  - **Response**: `[{ "id": 1, "timestamp": "2023-01-01T00:00:00.000Z", "text": "Received message here" }]`

## Support or Contributions
For support or contributions, please contact [email@example.com](mailto:email@example.com).
