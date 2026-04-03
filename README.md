# IdeasBot

A lightweight, secure, and private Telegram bot designed for quick brainstorming and idea logging. Perfect for developers who want to keep their thoughts organized in a simple text file on their own infrastructure.

![Preview](https://github.com/wpxq/ideas-bot/blob/main/ideasbot.png)

## Features
- **Private Access**: Restricts interaction to a specifix `user_id` using a custom `@restricted` decorator.
- **Simplicity**: Saves ideas directly to `ideas.txt`.
- **Dockerized**: Fully containerized setup with Docker Compose for seamless deployment.
- **Idea Managment**: Built-in commands to list and remove specific entries by index.

## Tech Stack
- **Lang**: Python 3.11
- **Library**: `python-telegram-bot`
- **Deployment**: Docker & Docker Compose

## Setup
1. Configuration:
Create a `.env` file based on `.env.example`:
```env
TOKEN=bot token
MYID=your user id
```
2. Run with docker
```bash
touch ideas.txt
docker compose up -d --build
```

## Commands
- `Any text` - Any other message is automatically saved as a new idea.
- `/start` - Initializes the bot and verified access.
- `/list` - Displays a numbered list of all saved ideas.
- `/remove <num>` - Deletes an idea based on its list index.
