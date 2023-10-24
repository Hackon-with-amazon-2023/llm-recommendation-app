# PIP INSTALL python-telegram-bot 

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.ext import filters , MessageHandler

# from langchain.llms import OpenAI
from .llm_prompts import LLM
from .chrome_driver import ChromeDriver



class TelegramBot:
    queries = {}

    def __init__(self, token: str, llm: LLM, driver: ChromeDriver) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.message_handler))
        # self.app.add_handler(CommandHandler("hello", self.start))
        self.app.add_handler(CommandHandler("start", self.start))
        # self.app.add_handler(CommandHandler("get_products", self.get_products))
        # self.app.add_handler(CommandHandler("reset_search_query", self.reset_search_query))

        self.app.add_handler(CallbackQueryHandler(self.get_product_details))
        
        self.llm = llm
        self.driver = driver

        self.reply_markup_remove = ReplyKeyboardRemove()

        ################################# MESSAGES #################################
        self.hello_message = ('Hello {name}, \n'
                                'I am here to help you with searching the products on amazon based on your requirements. '
                                'Please tell me what you are looking for.')
        
        self.get_product_details_message = ('Getting details for product with ASIN: {product_asin}. \n\n'
                                            "This can be implemented better using API, but for now you can open this link to see the product details:\n" + \
                                            "https://www.amazon.in/dp/{product_asin}")
        self.get_products_empty_query_message = ('Your search query is empty, ' 
                                                'before getting products from amazon please tell me what you are looking for.\n\n'
                                                'For example: Show me some laptops in range Rs. 30000 to 40000')
        self.reset_search_query_message = ('Hello {first_name}\n'
                                            'Your query has been reset, please tell me what you want to search on Amazon')
        self.message_handler_message = ('{query}\n\n'
                                            'Is this what you are looking for {name}?\n')



    ################################# FUNCTIONS #################################
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries or self.queries[update.effective_user.id] != "":
            self.queries[update.effective_user.id] = ""
        print("Bot started by: ", update.effective_user.username, update.effective_user.id)
        await update.message.reply_text(self.hello_message.format(name=update.effective_user.first_name),
                                        reply_markup=self.reply_markup_remove)
    


    async def get_products(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries or self.queries[update.effective_user.id] == "":    
            await update.message.reply_text(self.get_products_empty_query_message, 
                                            reply_markup=self.reply_markup_remove)
        else:
            await update.message.reply_text(f'Getting Products for query:\n{self.queries[update.effective_user.id]}', 
                                            reply_markup=self.reply_markup_remove)
            data = self.driver.scrape_products(self.queries[update.effective_user.id])

            scraped_data_message = "\n\n".join([str((i+1)) + ". " + str(data['product_names'][i]) for i in range(len(data['product_names'][:10]))])

            # keyboardButtons = [InlineKeyboardButton("Reset Search Query", callback_data="reset_search_query")]
            keyboardButtonsRow1, keyboardButtonsRow2 = [], []
            for i in range(len(data['product_names'][:5])):
                keyboardButtonsRow1.append(InlineKeyboardButton(f"{i+1}", callback_data=f"{data['product_asin'][i]}"))
            for i in range(5, len(data['product_names'][:10])):
                keyboardButtonsRow2.append(InlineKeyboardButton(f"{i+1}", callback_data=f"{data['product_asin'][i]}"))
            keyBoardMarkup = InlineKeyboardMarkup(inline_keyboard=[keyboardButtonsRow1, keyboardButtonsRow2])
            
            await update.message.reply_text('These are the products related to your query, click on the buttons to know more about product.\n' + \
                                                scraped_data_message, reply_markup=keyBoardMarkup)



    async def get_product_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        product_asin = update.callback_query.data
        # product_details = self.driver.get_product_details(product_asin)
        await update.callback_query.message.reply_text(self.get_product_details_message.format(product_asin=product_asin), 
                                                       reply_markup=self.reply_markup_remove)



    async def reset_search_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.queries[update.effective_user.id] = ""
        await update.message.reply_text(self.reset_search_query_message.format(first_name=update.effective_user.first_name),
                                        reply_markup=self.reply_markup_remove)



    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id not in self.queries:
            self.queries[update.effective_user.id] = ""
        
        new_text = update.message.text
        old_text = self.queries[update.effective_user.id]

        if new_text == "Yes, Get Products":
            await self.get_products(update, context)
            return
        elif new_text == "No, Update Query":
            await update.message.reply_text("Please send the follow up message to update your query",
                                            reply_markup=self.reply_markup_remove)
            return
        elif new_text == "Reset Search Query":
            await self.reset_search_query(update, context)
            return

        print("Text from:", update.effective_user.username, update.effective_user.id, "\nText:", new_text)
        self.queries[update.effective_user.id] = self.llm.get_user_query(old_query=old_text, new_message=new_text)

        if self.queries[update.effective_user.id] != "":
            reply_markup_keyboard_buttons = [[KeyboardButton(text="Yes, Get Products"), KeyboardButton(text="No, Update Query")], [KeyboardButton(text="Reset Search Query")]]
            reply_markup = ReplyKeyboardMarkup(reply_markup_keyboard_buttons, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(self.message_handler_message.format(query=self.queries[update.effective_user.id], name=update.effective_user.first_name), \
                                            reply_markup=reply_markup)
        else:
            await update.message.reply_text("Sorry, I am not able to understand what you are looking for. Please try again")
 



if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    llm = LLM(OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"))
    telegramBot = TelegramBot(token=os.getenv("telegram_token"), llm=llm)
    telegramBot.app.run_polling()
