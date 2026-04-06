#!/usr/bin/env python3
"""
💬 ChatBot-Agent
Chatbot Developer агент

Создаёт:
- Telegram ботов
- Discord ботов
- Slack ботов
- WhatsApp ботов
"""

import argparse
from pathlib import Path
from typing import Dict


class ChatBotAgent:
    """
    💬 ChatBot-Agent
    
    Специализация: Chatbot Development
    Платформы: Telegram, Discord, Slack, WhatsApp
    """
    
    NAME = "💬 ChatBot-Agent"
    ROLE = "Chatbot Developer"
    EXPERTISE = ["Telegram Bot", "Discord Bot", "Slack Bot", "WhatsApp Bot", "AI Assistants"]
    
    def process_request(self, request: str, platform: str = "telegram") -> Dict[str, str]:
        files = {}
        
        if platform == "discord":
            files = self._generate_discord_bot(request)
        elif platform == "slack":
            files = self._generate_slack_bot(request)
        else:
            files = self._generate_telegram_bot(request)
        
        return files
    
    def _generate_telegram_bot(self, feature: str) -> Dict[str, str]:
        files = {}
        
        files["bot.py"] = """import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (get from @BotFather)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Start command handler
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = f"👋 Hello, {message.from_user.full_name}!\\n\\n"
    welcome_text += "I'm your personal assistant bot. Here are available commands:\\n\\n"
    welcome_text += "/start - Start the bot\\n"
    welcome_text += "/help - Get help\\n"
    welcome_text += "/info - Get user info"
    
    await message.answer(welcome_text)

# Help command handler
@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = "📚 **Available Commands:**\\n\\n"
    help_text += "/start - Start the bot\\n"
    help_text += "/help - Show this help message\\n"
    help_text += "/info - Get your user information\\n"
    help_text += "/button - Show inline keyboard"
    
    await message.answer(help_text, parse_mode="Markdown")

# Info command handler
@dp.message(Command("info"))
async def cmd_info(message: Message):
    user = message.from_user
    info_text = "👤 **Your Information:**\\n\\n"
    info_text += f"ID: `{user.id}`\\n"
    info_text += f"Username: @{user.username or 'N/A'}\\n"
    info_text += f"Full Name: {user.full_name}\\n"
    info_text += f"Language: {user.language_code}"
    
    await message.answer(info_text, parse_mode="Markdown")

# Button command with inline keyboard
@dp.message(Command("button"))
async def cmd_button(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Yes", callback_data="yes")],
        [InlineKeyboardButton(text="❌ No", callback_data="no")],
        [InlineKeyboardButton(text="🔗 Open Link", url="https://example.com")]
    ])
    
    await message.answer("Choose an option:", reply_markup=keyboard)

# Callback handler
@dp.callback_query(F.data.in_(["yes", "no"]))
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "yes":
        await callback_query.answer("You selected YES!")
        await callback_query.message.edit_text("✅ You selected YES!")
    else:
        await callback_query.answer("You selected NO!")
        await callback_query.message.edit_text("❌ You selected NO!")

# Echo handler for text messages
@dp.message(F.text)
async def echo_message(message: Message):
    await message.answer(f"You said: {message.text}")

# Error handler
@dp.errors()
async def error_handler(update: types.Update, exception: Exception):
    logger.error(f"Error: {exception}")
    if update.message:
        await update.message.answer("❌ An error occurred. Please try again.")

async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        files["requirements.txt"] = """aiogram>=3.0.0
python-dotenv>=1.0.0
"""
        
        files[".env"] = """BOT_TOKEN=your_bot_token_here
"""
        
        return files
    
    def _generate_discord_bot(self, feature: str) -> Dict[str, str]:
        files = {}
        
        files["bot.py"] = """import discord
from discord.ext import commands
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
COMMAND_PREFIX = "!"

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for commands"
        )
    )

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    if channel:
        await channel.send(f"👋 Welcome to the server, {member.mention}!")

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'👋 Hello, {ctx.author.mention}!')

@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(
        title="Bot Information",
        description="Discord bot created by ChatBot-Agent",
        color=discord.Color.blue()
    )
    embed.add_field(name="Server", value=ctx.guild.name, inline=True)
    embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
    embed.set_footer(text=f"Requested by {ctx.author}")
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f'🗑️ Cleared {amount} messages')
    await asyncio.sleep(3)
    await msg.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use !help for available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    else:
        logger.error(f"Error: {error}")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
"""
        
        files["requirements.txt"] = """discord.py>=2.3.0
python-dotenv>=1.0.0
"""
        
        return files
    
    def _generate_slack_bot(self, feature: str) -> Dict[str, str]:
        files = {}
        
        files["bot.py"] = """import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("hello")
def say_hello(message, say):
    user = message['user']
    say(f"👋 Hi there, <@{user}>!")

@app.command("/info")
def handle_info_command(ack, command, say):
    ack()
    say({
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Bot Information"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Slack Bot* created by ChatBot-Agent"
                }
            }
        ]
    })

@app.event("app_mention")
def handle_app_mention(event, say):
    text = event.get('text', '').lower()
    
    if 'help' in text:
        say("Available commands: hello, info, help")
    else:
        say("👋 Hi! How can I help you today?")

if __name__ == "__main__":
    logger.info("Starting Slack bot...")
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
"""
        
        files["requirements.txt"] = """slack-bolt>=1.18.0
python-dotenv>=1.0.0
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="💬 ChatBot-Agent — Chatbots")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--platform", "-p", default="telegram", 
                       choices=["telegram", "discord", "slack", "whatsapp"])
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = ChatBotAgent()
    
    if args.request:
        print(f"💬 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request, args.platform)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"💬 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
