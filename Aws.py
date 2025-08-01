from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = '7964127387:AAHZ8x72Wh0OjNu92SS1V6XWzgLXHOq1vSU'  # Replace this with your actual bot token

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛍 Products", callback_data='products')],
        [InlineKeyboardButton("💎 Premium", callback_data='premium')],
        [InlineKeyboardButton("✅ Verify Payment", callback_data='verify')],
        [InlineKeyboardButton("📦 Track Order", callback_data='track')],
        [InlineKeyboardButton("🛠 Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("👋 Welcome to Amazon Deals Bot! Choose an option:", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'products':
        context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo='https://i.imgur.com/Lnk3YiS.jpg',
            caption="🔌 *Fast Charger* – ₹499\nHigh-speed USB-C fast charger.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data='buy_charger')],
                [InlineKeyboardButton("⬅️ Back", callback_data='back')]
            ])
        )
        context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo='https://i.imgur.com/xV9UwLk.jpg',
            caption="🎧 *Wireless Headphones* – ₹999\nLong battery life, noise cancellation.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data='buy_headphones')],
                [InlineKeyboardButton("⬅️ Back", callback_data='back')]
            ])
        )
        query.delete_message()

    elif query.data == 'premium':
        context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo='https://i.imgur.com/lBRceyq.jpg',
            caption="🕶️ *RayBan Sunglasses* – ₹2999\nPremium UV protection and style.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data='buy_glasses')],
                [InlineKeyboardButton("⬅️ Back", callback_data='back')]
            ])
        )
        context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo='https://i.imgur.com/YH1V9MY.jpg',
            caption="📱 *iPhone 14* – ₹74,999\nOriginal, sealed box with warranty.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy Now", callback_data='buy_iphone')],
                [InlineKeyboardButton("⬅️ Back", callback_data='back')]
            ])
        )
        query.delete_message()

    elif query.data == 'verify':
        query.edit_message_text("💳 Send your payment ID or screenshot to verify.")
    elif query.data == 'track':
        query.edit_message_text("📦 Enter your order ID to track it.")
    elif query.data == 'help':
        query.edit_message_text("🛠 Contact our support at @YourSupportUsername.")
    elif query.data == 'back':
        start(query, context)
    elif 'buy_' in query.data:
        product_name = query.data.replace('buy_', '').capitalize()
        query.edit_message_text(f"✅ You selected: {product_name}\n\n💳 Complete payment and send screenshot to verify.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
