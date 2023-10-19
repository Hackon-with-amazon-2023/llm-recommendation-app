# PIP INSTALL python-telegram-bot 

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import filters , MessageHandler
# from langchain.llms import OpenAI
from .llm_prompts import LLM



class TelegramBot:
    queries = {}
    app = None

    def __init__(self, token: str, llm: LLM) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.message_handler))
        self.app.add_handler(CommandHandler("hello", self.start))
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("get_products", self.get_products))
        self.app.add_handler(CommandHandler("reset_search_query", self.reset_search_query))

        self.llm = llm



    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries or self.queries[update.effective_user.id] != "":
            self.queries[update.effective_user.id] = ""
        print("Bot started by: ", update.effective_user.first_name, update.effective_user.id)
        await update.message.reply_text(f'Hello {update.effective_user.first_name}, \n'
                                        'I am here to help you with searching the products on amazon based on your requirements. '
                                        'Please tell me what you are looking for.')



    async def get_products(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries or self.queries[update.effective_user.id] == "":    
            await update.message.reply_text('Your search query is empty, ' 
                                            'before getting products from amazon please tell me what you are looking for.\n\n'
                                            'For example: Show me some laptops in range Rs. 30000 to 40000')
        else:
            await update.message.reply_text(f'Getting Products for query:\n{self.queries[update.effective_user.id]}')



    async def reset_search_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.queries[update.effective_user.id] = ""
        await update.message.reply_text(f'Hello {update.effective_user.first_name}\n'
                                        'Your query has been reset, please tell me what you want to search on Amazon')



    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries:
            self.queries[update.effective_user.id] = ""
        
        new_text = update.message.text
        old_text = self.queries[update.effective_user.id]

        print("Text from:", update.effective_user.id, "\nText:", new_text)
        self.queries[update.effective_user.id] = self.llm.get_user_query(old_query=old_text, new_message=new_text)
        await update.message.reply_text(f'{self.queries[update.effective_user.id]}' + 
                                        f'\n\nIs this what you are looking for {update.effective_user.first_name}?\n'
                                        'If the following query is correct then please click /get_products\n'
                                        'if you want to update the query then please send the follow up message\n'
                                        'and if your query is entirely wrong then please click /reset_search_query')
 



if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    telegramBot = TelegramBot(token=os.getenv("telegram_token"))
    telegramBot.app.run_polling()
