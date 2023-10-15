################################# IMPORTS #################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from webdriver_manager.chrome import ChromeDriverManager





################################# CREATE DRIVER #################################
options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)





################################# FUNCTIONS #################################

def driver_alive(driver):
    try:
        driver.title
    except Exception:
        return False
    return driver


def get_driver():
    global driver
    if not driver_alive(driver):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver



def scrape_products(driver, keyword):
    if not driver_alive(driver):
        driver = get_driver()
    
    if "amazon.com" not in driver.current_url or "amazon.in" not in driver.current_url:
        driver.get("https://www.amazon.com")

    # create WebElement for a search box
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys(keyword)

    # create WebElement for a search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    search_button.click()

    # wait for the page to download
    driver.implicitly_wait(5)

    # Get the data
    product_name = []
    product_asin = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []

    items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)
        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

    # following return statement is for checking that we correctly scrape data we want
    return {
        "product_names": product_name,
        "product_asin": product_asin
    }




def quit_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        print(e)
