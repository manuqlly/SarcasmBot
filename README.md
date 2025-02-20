# Discord Message Parser and Chatbot

This project is a Discord message parser and chatbot that fetches messages from a Discord server, stores them in a PostgreSQL database, processes them using FAISS for similarity search, and uses a chatbot to respond to user queries. The chatbot's accuracy depends on the content of the chats.

## Features

- Fetch messages from a Discord server and store them in a PostgreSQL database.
- Process messages using FAISS for similarity search.
- Use a chatbot to respond to user queries with witty, sarcastic, or funny responses.
- Open source under the MIT License.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Discord Developer Bot (Create a bot [here](https://discord.com/developers/applications))

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/discord-message-parser-chatbot.git
    cd discord-message-parser-chatbot
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL:**

    Create a PostgreSQL database and update the [DATABASE_URL](http://_vscodecontentref_/0) in [fais.py](http://_vscodecontentref_/1) and [msg.py](http://_vscodecontentref_/2) with your database credentials.

4. **Set up Discord Bot:**

    Create a Discord bot and get the bot token. Update the [DISCORD_TOKEN](http://_vscodecontentref_/3) in [my_discord_bot.py](http://_vscodecontentref_/4) and [TOKEN](http://_vscodecontentref_/5) in [msg.py](http://_vscodecontentref_/6) with your bot token.

5. **Run the message fetcher:**

    ```sh
    python msg.py
    ```

    This will fetch all messages from the specified Discord channel and store them in the PostgreSQL database.

6. **Process messages and store embeddings in FAISS:**

    ```sh
    python fais.py
    ```

    This will fetch messages from the database, process them in batches, and store the embeddings in a FAISS index.

7. **Run the Discord chatbot:**

    ```sh
    python my_discord_bot.py
    ```

    This will start the Discord bot, which will respond to user queries based on the processed messages.

## File Structure

- [msg.py](http://_vscodecontentref_/7): Fetches messages from a Discord server and stores them in a PostgreSQL database.
- [fais.py](http://_vscodecontentref_/8): Processes messages from the database and stores embeddings in a FAISS index.
- [my_discord_bot.py](http://_vscodecontentref_/9): Discord bot that responds to user queries using the FAISS index and a chatbot.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [Discord Developer Portal](https://discord.com/developers/applications)
- [FAISS](https://github.com/facebookresearch/faiss)
