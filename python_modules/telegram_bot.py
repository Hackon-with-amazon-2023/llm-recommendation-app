# PIP INSTALL python-telegram-bot 

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.ext import filters , MessageHandler

# from langchain.llms import OpenAI
from .llm_prompts import LLM
from .scrape_products import ChromeDriver



class TelegramBot:
    queries = {}

    def __init__(self, token: str, llm: LLM, driver: ChromeDriver) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.message_handler))
        self.app.add_handler(CommandHandler("hello", self.start))
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("get_products", self.get_products))
        self.app.add_handler(CommandHandler("reset_search_query", self.reset_search_query))

        self.app.add_handler(CallbackQueryHandler(self.get_product_details))

        self.llm = llm
        self.driver = driver



    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries or self.queries[update.effective_user.id] != "":
            self.queries[update.effective_user.id] = ""
        print("Bot started by: ", update.effective_user.first_name, update.effective_user.id)
        await update.message.reply_text(f'Hello {update.effective_user.first_name}, \n'
                                        'I am here to help you with searching the products on amazon based on your requirements. '
                                        'Please tell me what you are looking for.')
    

    async def get_product_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        product_asin = update.callback_query.data
        # product_details = self.driver.get_product_details(product_asin)
        await update.callback_query.message.reply_text(f'Getting details for product with ASIN: {product_asin}. \n\n'
                                                       "This can be implemented better using API, but for now you can open this link to see the product details:\n" + \
                                                       f"https://www.amazon.in/dp/{product_asin}")



    async def get_products(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries or self.queries[update.effective_user.id] == "":    
            await update.message.reply_text('Your search query is empty, ' 
                                            'before getting products from amazon please tell me what you are looking for.\n\n'
                                            'For example: Show me some laptops in range Rs. 30000 to 40000')
        else:
            await update.message.reply_text(f'Getting Products for query:\n{self.queries[update.effective_user.id]}')
            data = self.driver.scrape_products(self.queries[update.effective_user.id])

            scraped_data_message = "\n\n".join([str((i+1)) + ". " + str(data['product_names'][i]) for i in range(len(data['product_names'][:10]))])

            # keyboardButtons = [InlineKeyboardButton("Reset Search Query", callback_data="reset_search_query")]
            keyboardButtonsRow1, keyboardButtonsRow2 = [], []
            for i in range(len(data['product_names'][:5])):
                keyboardButtonsRow1.append(InlineKeyboardButton(f"{i+1}", callback_data=f"{data['product_asin'][i]}"))
            for i in range(5, len(data['product_names'][:10])):
                keyboardButtonsRow2.append(InlineKeyboardButton(f"{i+1}", callback_data=f"{data['product_asin'][i]}"))
            keyBoardMarkup = InlineKeyboardMarkup(inline_keyboard=[keyboardButtonsRow1, keyboardButtonsRow2])
            
            await update.message.reply_text('Scraped products:\n' + scraped_data_message, reply_markup=keyBoardMarkup)
            await update.message.reply_text('These are the products related to your query, click on the buttons to know more about product.')



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
        if self.queries[update.effective_user.id] != "":
            await update.message.reply_text(f'{self.queries[update.effective_user.id]}' + 
                                            f'\n\nIs this what you are looking for {update.effective_user.first_name}?\n'
                                            'If the following query is correct then please click /get_products\n'
                                            'if you want to update the query then please send the follow up message\n'
                                            'and if your query is entirely wrong then please click /reset_search_query')
        else:
            await update.message.reply_text("Sorry, I am not able to understand what you are looking for. Please try again")
 



if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    llm = LLM(OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"))
    telegramBot = TelegramBot(token=os.getenv("telegram_token"), llm=llm)
    telegramBot.app.run_polling()
