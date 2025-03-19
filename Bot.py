import discord
import sqlite3
import re
from discord.ext import commands
import os
TOKEN = os.getenv("TOKEN")
from keep_alive import keep_alive
keep_alive()


# Configuration

STORAGE_CHANNEL_ID = 123456789012345678  # Replace with your link-sharing channel ID
RESPONSE_CHANNEL_ID = 123456789012345678  # Replace with your response channel ID
ALLOWED_ROLE = "Student"  # Replace with the role allowed to use the bot

# Setup bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Database setup
conn = sqlite3.connect("links.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, keyword TEXT, url TEXT)''')
conn.commit()

# Function to extract links
def extract_links(text):
    return re.findall(r'(https?://\S+)', text)

# Event: Store links when a message is sent in the storage channel
@bot.event
async def on_message(message):
    if message.channel.id == STORAGE_CHANNEL_ID and message.author != bot.user:
        links = extract_links(message.content)
        for link in links:
            keyword = message.content.replace(link, "").strip().lower()  # Use the rest as keyword
            c.execute("INSERT INTO links (keyword, url) VALUES (?, ?)", (keyword, link))
            conn.commit()
        await message.add_reaction("✅")  # Confirmation emoji
    await bot.process_commands(message)

# Command: Retrieve links based on keywords
@bot.command()
async def get(ctx, *, keyword: str):
    if ctx.channel.id != RESPONSE_CHANNEL_ID:
        return  # Ignore messages outside response channel

    # Check if user has the allowed role
    if ALLOWED_ROLE not in [role.name for role in ctx.author.roles]:
        await ctx.send("❌ You do not have permission to use this command.")
        return

    c.execute("SELECT url FROM links WHERE keyword=?", (keyword.lower(),))
    results = c.fetchall()

    if results:
        response = "\n".join([row[0] for row in results])
        await ctx.send(f"📚 Here are the links for **{keyword}**:\n{response}")
    else:
        await ctx.send("❌ No links found for that keyword.")

# Run the bot
bot.run(TOKEN)
