from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
import asyncio

BOT_TOKEN = "8340122633:AAFhQoNFXc4JhO3gr7qd8OJUZkEI6vXAT4k"
ADMIN_ID = 8013386904
CHANNEL_ID = "-1002860977591"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Feedback Bot!\n"
        "Use /feedback <message> to share your thoughts.\n"
        "Send photo/video/file — it will be forwarded in 5 minutes."
    )

# /feedback
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("❗ Use: /feedback your_message")
        return

    user = update.effective_user.mention_html()
    chat_title = update.message.chat.title or "Private"
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted = (
        "📩 <b>New Feedback Received!</b>\n"
        f"👤 <b>From:</b> {user}\n"
        f"💬 <b>Chat:</b> {chat_title}\n"
        f"🕒 <b>Time:</b> {time_str}\n\n"
        f"💬 <b>Feedback:</b>\n{msg}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=formatted, parse_mode="HTML")
    await context.bot.send_message(chat_id=CHANNEL_ID, text=formatted, parse_mode="HTML")
    await update.message.reply_text("✅ Feedback sent!")

# Media forwarder
async def forward_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Media received! Forwarding in 5 minutes...")
    await asyncio.sleep(300)

    try:
        await update.message.copy(chat_id=ADMIN_ID)
        await update.message.copy(chat_id=CHANNEL_ID)
        await update.message.reply_text("✅ Media forwarded.")
    except Exception as e:
        await update.message.reply_text("⚠️ Error forwarding media.")
        print("Error:", e)

# App setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("feedback", feedback))
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.DOCUMENT, forward_media))

# Start the bot
app.run_polling()