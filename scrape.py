from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import atexit
from opendata import OpenData

driver = webdriver.Chrome()
driver.implicitly_wait(7)

base_path = "https://nocopo.bpp.gov.ng/OpenData.aspx"
print_button_id = "#ctl00_ContentPlaceHolder1_ButtonPrint"

driver.get(base_path)
table_driver = OpenData(driver)
atexit.register(table_driver.cleanup)
table_driver.navigate_to_page()


