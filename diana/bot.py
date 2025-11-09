from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from diana.settings import (
    TELEGRAM_TOKEN,
    PROXY_URL,
    logger
)



# TODO: Complte help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hi {update.effective_user.first_name}! 👋')


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"you sent: {update.message.text}")


def run_bot():

    builder =  ApplicationBuilder().token(TELEGRAM_TOKEN)

    if PROXY_URL:
        builder = (
            builder
            .proxy(PROXY_URL)
            .get_updates_proxy(PROXY_URL)
        )

    app = builder.build()

    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    logger.info("Diana Starting ...")

    app.run_polling()
