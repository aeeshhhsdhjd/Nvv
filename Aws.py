from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    CallbackContext
)
import logging

# === CONFIG ===
BOT_TOKEN = "7964127387:AAFusDYZrqWyv1EpAqtUu4Hw2EltHzCA-40"
ADMIN_CHAT_ID = 6829160614  # Replace with your Telegram user ID or private group ID
AFFILIATE_TAG = "yourtag-21"  # Your Amazon Affiliate Tag

# === LOGGING ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# === MAIN KEYBOARD ===
main_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("/product"), KeyboardButton("/verify")],
    [KeyboardButton("/help"), KeyboardButton("/about")]
], resize_keyboard=True)

# === START ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to Amazon Product Bot!\n\nUse the buttons below to begin.",
        reply_markup=main_keyboard
    )

# === HELP ===
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🛠 *Bot Commands:*\n"
        "/product – Search Amazon product\n"
        "/verify – Send UPI screenshot\n"
        "/about – About this bot",
        parse_mode="Markdown"
    )

# === ABOUT ===
def about(update: Update, context: CallbackContext):
    update.message.reply_text(
        "ℹ️ This bot helps users find Amazon products and submit UPI payment proofs.\n"
        "Built in Python using python-telegram-bot."
    )

# === PRODUCT SEARCH (MOCK) ===
def product(update: Update, context: CallbackContext):
    query = " ".join(context.args) if context.args else "Sample Product"
    
    # Mock Amazon product
    product_title = f"{query} – Example"
    product_price = "₹999"
    product_image = "https://via.placeholder.com/300"
    product_link = f"https://www.amazon.in/dp/B09G9F54RJ/?tag={AFFILIATE_TAG}"
    
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 Buy on Amazon", url=product_link)]
    ])

    update.message.reply_photo(
        photo=product_image,
        caption=f"🛒 *{product_title}*\n💰 Price: {product_price}",
        parse_mode="Markdown",
        reply_markup=inline_keyboard
    )

# === PAYMENT VERIFICATION INFO ===
def verify(update: Update, context: CallbackContext):
    update.message.reply_text(
        "💳 Please send your *UPI payment screenshot* here.\n\n"
        "Pay to: `your-upi@okaxis`\n"
        "After payment, send the photo or file and it will be auto-forwarded to admin.",
        parse_mode="Markdown"
    )

# === AUTO-FORWARD MEDIA TO ADMIN ===
def forward_payment_proof(update: Update, context: CallbackContext):
    message = update.message
    user = message.from_user
    caption = f"📥 *Payment Proof*\nFrom: {user.first_name} (@{user.username})\nUser ID: `{user.id}`"

    try:
        if message.photo:
            photo = message.photo[-1].file_id
            context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo, caption=caption, parse_mode="Markdown")
        elif message.document:
            document = message.document.file_id
            context.bot.send_document(chat_id=ADMIN_CHAT_ID, document=document, caption=caption, parse_mode="Markdown")
        elif message.video:
            video = message.video.file_id
            context.bot.send_video(chat_id=ADMIN_CHAT_ID, video=video, caption=caption, parse_mode="Markdown")
        else:
            message.reply_text("❌ Please send a photo, document, or video as payment proof.")
            return

        message.reply_text("✅ Payment proof received. We'll verify and contact you soon.")
    except Exception as e:
        logger.error(f"Error forwarding: {e}")
        message.reply_text("⚠️ Error sending proof. Please try again.")

# === UNKNOWN COMMAND HANDLER ===
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("❓ Unknown command. Use /help for list of options.")

# === MAIN FUNCTION ===
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("verify", verify))
    dp.add_handler(CommandHandler("product", product))

    # Auto-forward media
    dp.add_handler(MessageHandler(Filters.photo | Filters.document | Filters.video, forward_payment_proof))

    # Unknown commands
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
