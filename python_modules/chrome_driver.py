################################# IMPORTS #################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from webdriver_manager.chrome import ChromeDriverManager





class ChromeDriver:
    ################################# CREATE DRIVER #################################
    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--headless')
        self.options.add_argument("user-data-dir=selenium_user_data")


        self.driver = None
        self.driver = self.get_driver()



    ################################# FUNCTIONS #################################
    def get_driver(self):
        if not self.is_driver_alive():
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        return self.driver


    def is_driver_alive(self):
        try:
            self.driver.title
        except Exception:
            return False
        return True


    def scrape_products(self, keyword):
        if not self.is_driver_alive():
            self.driver = self.get_driver()
        try:
            # if "amazon.com" not in self.driver.current_url and "amazon.in" not in self.driver.current_url:
            if len(self.driver.find_elements(By.ID, 'twotabsearchtextbox')) == 0:
                self.driver.get("https://www.amazon.com")

            if len(self.driver.find_elements(By.CSS_SELECTOR, "form[action='/errors/validateCaptcha']")):
                print("Captcha found")
                return {
                    "type": "Captcha",
                    "product_names": ["Captcha found", "Please contact owner or try again later"],
                    "image": self.driver.find_element(By.CSS_SELECTOR, "form[action='/errors/validateCaptcha']>img").get_attribute("src")
                }

            # create WebElement for a search box
            search_box = self.driver.find_element(By.ID, 'twotabsearchtextbox')
            search_box.send_keys(keyword)

            # create WebElement for a search button
            search_button = self.driver.find_element(By.ID, 'nav-search-submit-button')
            search_button.click()

            # wait for the page to download
            self.driver.implicitly_wait(5)

            # Get the data
            product_name = []
            product_asin = []
            product_price = []
            product_ratings = []
            product_ratings_num = []
            product_link = []

            items = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            for item in items:
                try:
                    name = item.find_element(By.CSS_SELECTOR, 'span.a-text-normal.a-color-base')
                    data_asin = item.get_attribute("data-asin")
                    product_name.append(name.text)
                    product_asin.append(data_asin)
                except Exception as e:
                    print("Name not found")

            # following return statement is for checking that we correctly scrape data we want
            return {
                "type": "success",
                "product_names": product_name,
                "product_asin": product_asin
            }
        except Exception as e:
            print(e)
            return {
                "type": "error",
                "product_names": ["An error occured while scraping products", "Please contact owner or try again later"],
            }
    
    def quit_driver(self, driver):
        try:
            self.driver.quit()
        except Exception as e:
            print(e)
