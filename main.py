from python_modules.scrape_products import get_driver, driver_alive, scrape_products, quit_driver
from python_modules.telegram_bot import start_telegram_bot

from dotenv import load_dotenv
import os


load_dotenv()

driver = get_driver()
app = start_telegram_bot(token=os.getenv("telegram_token"))


data = scrape_products(driver, "Air Conditionor")
print(data)



app.run_polling()
quit_driver(driver)
