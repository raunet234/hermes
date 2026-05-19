import os
import re
import subprocess
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are Hermes, an AI agent that controls a Hedera blockchain CLI tool.
When a user sends you a message, respond with ONLY the exact command to pass to launch.sh, nothing else.
Available commands:
- balance
- price HBAR
- price USDC
- status
- tokens
- history
- help
If you cannot map the user request to a command, respond with: UNKNOWN
Always respond with just the command, no explanation, no punctuation."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Hermes Agent!\n\n"
        "I'm your AI-powered Hedera blockchain assistant.\n"
        "Powered by Gemini AI + Hedera testnet.\n\n"
        "Try asking me:\n"
        "• Check my balance\n"
        "• What is the price of HBAR?\n"
        "• Show my transaction history\n"
        "• Show all my tokens\n\n"
        "Type /help for more info."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hermes Agent — What you can ask:\n\n"
        "💰 Portfolio\n"
        "• Check my balance\n"
        "• Show my tokens\n"
        "• Show transaction history\n\n"
        "📈 Prices\n"
        "• What is the price of HBAR?\n"
        "• USDC price\n\n"
        "⚙️ System\n"
        "• System status\n"
        "• Help\n\n"
        "Just type naturally — I understand plain English!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    thinking_msg = await update.message.reply_text("⏳ Thinking...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\n\nUser: " + user_message
        )
        command = response.text.strip()

        if command == "UNKNOWN":
            await thinking_msg.edit_text("❓ Sorry, I didn't understand that. Try asking about your balance, token prices, or transaction history.")
            return

        result = subprocess.run(
            ["./launch.sh"] + command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip() or result.stderr.strip() or "No output returned."
        # Strip ANSI color codes
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        output = re.sub(r'\[[\d;]*m', '', output)
        await thinking_msg.edit_text(f"✅ Command: {command}\n\n{output}")

    except subprocess.TimeoutExpired:
        await thinking_msg.edit_text("⏰ Command timed out after 30 seconds.")
    except Exception as e:
        await thinking_msg.edit_text(f"❌ Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Hermes Agent is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
