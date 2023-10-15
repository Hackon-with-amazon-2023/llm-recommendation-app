# PIP INSTALL python-telegram-bot 

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import filters , MessageHandler



queries = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in queries or queries[update.effective_user.id] != "":
        queries[update.effective_user.id] = ""
    print("Bot started by: ", update.effective_user.first_name, update.effective_user.id)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, \n'
                                    'I am here to help you with searching the products on amazon based on your requirements. '
                                    'Please tell me what you are looking for.')



async def get_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in queries or queries[update.effective_user.id] == "":    
        await update.message.reply_text('Your search query is empty, ' 
                                        'before getting products from amazon please tell me what you are looking for.\n\n'
                                        'For example: Show me some laptops in range Rs. 30000 to 40000')
    else:
        await update.message.reply_text(f'Getting Products for query:\n{queries[update.effective_user.id]}')



async def reset_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    queries[update.effective_user.id] = ""
    await update.message.reply_text(f'Hello {update.effective_user.first_name}\n'
                                    'Your query has been reset, please tell me what you want to search on Amazon')



async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print("Text from:", update.effective_user.id, "\nText:", text)
    if update.effective_user.id not in queries:
        queries[update.effective_user.id] = ""
    queries[update.effective_user.id] += text
    await update.message.reply_text(f'{queries[update.effective_user.id]}' + 
                                    f'\n\nIs this what you are looking for {update.effective_user.first_name}?\n'
                                    'If the following query is correct then please click /get_products\n'
                                    'if you want to update the query then please send the follow up message\n'
                                    'and if your query is entirely wrong then please click /reset_search_query')



def start_telegram_bot(token):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    app.add_handler(CommandHandler("hello", start))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_products", get_products))
    app.add_handler(CommandHandler("reset_search_query", reset_search_query))
    return app



if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    app = start_telegram_bot(os.getenv("telegram_token"))
    app.run_polling()
