# HR LLM Chatbot Task

This repository contains a FastAPI application that serves as a simple chatbot API. The chatbot has basic functionality to respond to user messages and keep track of conversation history.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- OpenAI API Key

### Setup

1. **Configure Environment Variables:**

   Copy the `.env.example` file to `.env` and fill in the necessary OpenAI API keys.

### Building and Running the Application

Use Docker Compose to build and start the FastAPI app. This will set up the necessary environment and start the application on `http://127.0.0.1:8000`.

### API Endpoints

The application provides the following endpoints:

#### 1. `POST http://127.0.0.1:8000/api/conversation/respond`

This endpoint allows you to send a message to the chatbot and get a response.

- **Request Body:**

  ```json
  {
      "include_personal_information": true,
      "message": "hello"
  }
    ```
- **`include_personal_information`**: A boolean flag that controls whether mock user information should be included in the chatbot's description.
- **`message`**: The user's message to the chatbot.

#### 2. `GET http://127.0.0.1:8000/api/messages`

This endpoint retrieves the entire active conversation's messages.

### Restarting the Chat

To restart the chat, you need to reboot the Docker container. This is necessary because full chat functionality, such as conversation resetting, was not implemented due to time constraints.
