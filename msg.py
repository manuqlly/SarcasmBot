import bot
import asyncpg
import asyncio
import os
from tqdm.asyncio import tqdm  # Import async progress bar

TOKEN = "DISCORD_BOT_TOKEN"
GUILD_ID = 11646466132#serverID 
CHANNEL_ID = 42151535631#channelID

DB_URL = "postgresql://postgres:root@localhost/discord_bot"

intents = bot.Intents.default()
intents.message_content = True
client = bot.Client(intents=intents)

async def store_messages(messages):
    if not messages:
        print("No messages to store.")
        return

    conn = await asyncpg.connect(DB_URL)
    async with conn.transaction():
        for message in tqdm(messages, desc="Storing Messages", unit="msg"):
            if message.content:
                try:
                    await conn.execute(
                        """
                        INSERT INTO discord_messages (id, user_id, content, timestamp) 
                        VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO NOTHING
                        """,
                        message.id, message.author.id, message.content, message.created_at
                    )
                except Exception as e:
                    print(f"Database error: {e}")
    await conn.close()
    print(f"Stored {len(messages)} messages in the database.")

async def fetch_all_messages(channel):
    all_messages = []
    try:
        async for message in tqdm(channel.history(limit=None), desc="Fetching Messages", unit="msg"):
            all_messages.append(message)
    except bot.errors.Forbidden:
        print("Bot lacks permission to read message history!")
    except Exception as e:
        print(f"Error fetching messages: {e}")
    
    print(f"Fetched {len(all_messages)} messages.")
    return all_messages

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await asyncio.sleep(5)  # Ensure bot is fully ready

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Channel with ID {CHANNEL_ID} not found!")
        return

    messages = await fetch_all_messages(channel)  # Fetch all messages
    await store_messages(messages)
    print("Messages stored successfully!")

client.run(TOKEN)
