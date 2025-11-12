from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from langchain_core.messages.human import HumanMessage

from diana.settings import (
    TELEGRAM_TOKEN,
    PROXY_URL,
    OWNER_USERNAME,
    logger
)

from diana.agent import agent


# TODO: Complte help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hi {update.effective_user.first_name}! 👋')


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username == OWNER_USERNAME:
        user_message = HumanMessage(update.message.text)
        reply_message = await agent.ainvoke({"messages": user_message})
        await update.message.reply_text(reply_message["messages"][-1].content)
    
    # TODO: Handle if it is not owner
    else: 
        ...


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
