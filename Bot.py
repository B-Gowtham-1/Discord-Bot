import discord
from discord.ext import commands
import os
TOKEN = os.getenv("TOKEN")
# Configuration
STORAGE_CHANNEL_ID = 1351481296731508756 # Replace with your link-storage channel ID
RESPONSE_CHANNEL_ID = 1351577625403064432  # Replace with your response channel ID
ALLOWED_ROLE = "Member"  # Role required to use the bot

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Ensure message content intent is enabled

bot = commands.Bot(command_prefix="!", intents=intents)

# Command: Search for messages with keyword in the storage channel
@bot.command()
async def get(ctx, *, keyword: str):
    if ctx.channel.id != RESPONSE_CHANNEL_ID:
        return  # Ignore if command is used outside the response channel

    # Check if user has the required role
    if ALLOWED_ROLE not in [role.name for role in ctx.author.roles]:
        await ctx.send("❌ You do not have permission to use this command.")
        return

    storage_channel = bot.get_channel(STORAGE_CHANNEL_ID)
    if not storage_channel:
        await ctx.send("❌ Could not access the storage channel.")
        return

    messages_found = []
    
    # Search messages in the storage channel
    async for message in storage_channel.history(limit=100):  # Adjust limit if needed
        if keyword.lower() in message.content.lower():
            messages_found.append(f"🔹 {message.author.display_name}: {message.content}")

    # Send the results
    if messages_found:
        response = "\n\n".join(messages_found)
        await ctx.send(f"📚 Messages containing **{keyword}**:\n{response}")
    else:
        await ctx.send("❌ No messages found with that keyword.")

# Run the bot
  # Replace with your bot token
bot.run(TOKEN)
