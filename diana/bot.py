import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from diana.settings import settings


from diana.agent import run_agent


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    system_message = SystemMessage(
        "The user wants to know about you and your abilities. introduce about yourself."
        " this is should be like a help page. Use the language most commonly used by the user."
    )

    ai_response = await run_agent(thread_id=update.effective_user.id,
                                  message=system_message) 

    await update.message.reply_text(ai_response["messages"][-1].content)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    if update.effective_user.username == settings.OWNER_USERNAME:
        
        message = HumanMessage(update.message.text)

        agent_response = await run_agent(thread_id=update.effective_user.id,
                                         message=message)
 
        await update.message.reply_text(agent_response["messages"][-1].content)
    
    # TODO: Handle if it is not owner
    else: 
        ...


def run_bot():

    builder =  ApplicationBuilder().token(settings.TELEGRAM_TOKEN)

    if settings.PROXY_URL:
        builder = (
            builder
            .proxy(settings.PROXY_URL)
            .get_updates_proxy(settings.PROXY_URL)
        )

    app = builder.build()

    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    logging.info("Diana Starting ...")

    app.run_polling()
