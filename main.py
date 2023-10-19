from python_modules.scrape_products import get_driver, driver_alive, scrape_products, quit_driver
from python_modules.telegram_bot import TelegramBot
from python_modules.llm_prompts import LLM

from dotenv import load_dotenv
import os


load_dotenv()

driver = get_driver()
llm = LLM(OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"))
telegramBot = TelegramBot(token=os.getenv("telegram_token"), llm=llm)


data = scrape_products(driver, "Air Conditionor")
print(data)



telegramBot.app.run_polling()
quit_driver(driver)
