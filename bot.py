import telebot
from config import BOT_TOKEN, AUTO_REPLY_MESSAGE

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    """
    سلام من زیاد نمیام توی تلگرام ، اگر کار مهمی داری لطفا یه جای دیگه پیام بده
    """
    try:
        # Send the auto-reply message
        bot.reply_to(message, AUTO_REPLY_MESSAGE)
        print(f"Sent auto-reply to user {message.from_user.username} (ID: {message.from_user.id})")
    except Exception as e:
        print(f"Error sending message: {e}")

def main():
    print("Bot started! Press Ctrl+C to exit.")
    try:
        # Start the bot
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    main()