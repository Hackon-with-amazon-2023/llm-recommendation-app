from python_modules.scrape_products import get_driver, driver_alive, scrape_products, quit_driver


driver = get_driver()
data = scrape_products(driver, "Air Conditionor")
print(data)
quit_driver(driver)
