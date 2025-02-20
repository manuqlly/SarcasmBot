import discord
import asyncio
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import random

# 🔑 Set your API keys
DISCORD_TOKEN = "YOUR_DISCORD_API"
GEMINI_API_KEY = "YOUR_GEMINI_API"

# ✅ Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

# ✅ Load FAISS index
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# ✅ Discord bot setup
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages

    if client.user in message.mentions:  # If bot is mentioned
        query = message.content.replace(f"<@{client.user.id}>", "").strip()
        if not query:
            return

        try:
            # 🔎 Search FAISS for similar messages
            docs = vector_store.similarity_search(query, k=3)
            retrieved_texts = [doc.page_content for doc in docs] if docs else []

            if retrieved_texts:
                prompt = ("Make this response sarcastic, witty, or funny: "
                          f"Past responses: {retrieved_texts}\nUser query: {query}")
            else:
                prompt = ("User said: " + query +
                          "\nRespond with something funny, sarcastic, or clever.")

            # 🧠 Generate a response using Gemini
            response = gemini_model.generate_content(prompt)
            reply = response.text.strip() if response.text else "I don't know how to respond to that."

            # Add random variations to avoid repetition
            fun_variations = [
                "Oh wow, what a groundbreaking thought!", 
                "I’m just a bot, but even I felt that one.",
                "Hold on, let me roll my digital eyes...", 
                "Ah yes, the wisdom of the internet strikes again!",
                "Congratulations, you have my full robotic attention."
            ]
            if random.random() < 0.3:  # 30% chance to add a funny remark
                reply += "\n" + random.choice(fun_variations)

            await message.channel.send(reply)

        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("I'm having trouble finding a response right now, maybe try speaking in binary?")

# 🚀 Run the bot
client.run(DISCORD_TOKEN)
