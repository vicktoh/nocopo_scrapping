from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import atexit
from daudu import Daudu

driver = webdriver.Chrome()
driver.implicitly_wait(7)

base_path = "https://nocopo.bpp.gov.ng/noc/frmCitizenDashBoard.aspx"
print_button_id = "#ctl00_ContentPlaceHolder1_ButtonPrint"

driver.get(base_path)
table_driver = Daudu(driver)
atexit.register(table_driver.cleanup)
data_tuple = table_driver.table_all()

table_file = open("newdata/table_data.json", 'w')
details_file = open('newdata/details.json', 'w')

details_json = json.dumps(data_tuple[1])
table_json = json.dumps(data_tuple[0])

table_file.write(table_json)
details_file.write(table_json)

table_file.close()
details_file.close()

print("Done scrapping NOCOPO")





