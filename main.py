from python_modules.scrape_products import ChromeDriver
from python_modules.telegram_bot import TelegramBot
from python_modules.llm_prompts import LLM
from keep_bot_alive import keep_alive

from dotenv import load_dotenv
import os


load_dotenv()
keep_alive()

driver = ChromeDriver()
llm = LLM(OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"))
telegramBot = TelegramBot(token=os.getenv("TELEGRAM_TOKEN"), llm=llm, driver=driver)


data = driver.scrape_products("Air Conditionor")
print(data)



telegramBot.app.run_polling()
driver.quit_driver(driver)
