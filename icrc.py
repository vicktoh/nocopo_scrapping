from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import atexit

driver = webdriver.Chrome()
driver.implicitly_wait(7)

base_path = "https://ppp.icrc.gov.ng/"

driver.get(base_path)

data = []


def get_table(driver):
    rows = driver.find_elements_by_css_selector("#projects-table > tbody > tr")
    pages = driver.find_elements_by_css_selector("#projects-table_paginate > span > a")
    data = []
    for i in range(1,len(pages)):
        for j in range(len(rows)):
            row = driver.find_elements_by_css_selector("#projects-table > tbody > tr")[j]
            rowdata = extract_data(row)
            row.click()
            WebDriverWait(driver, 22).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#project-title-m")))
            rowdata.append(driver.current_url)
            data.append(rowdata)
            print(rowdata)
            driver.back()
            WebDriverWait(driver, 22).until(EC.invisibility_of_element((By.CSS_SELECTOR, "#projects-table_processing")))
            driver.find_elements_by_css_selector("#projects-table_paginate > span > a")[i-1].click()
            WebDriverWait(driver, 22).until(EC.invisibility_of_element((By.CSS_SELECTOR, "#projects-table_processing")))
        nexpage = driver.find_elements_by_css_selector("#projects-table_paginate > span > a")[i]
        nexpage.click()
        WebDriverWait(driver, 22).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#projects-table_paginate span a:nth-child(%s).current"%(i+1))))
    file = open("icrcdatalink.json", "w")
    icrcjson = json.dumps(data)
    file.write(icrcjson)


    

def extract_data(row):
    celldata = []
    cells = row.find_elements_by_css_selector("td")
    numcells = len(cells)
    for i in range(numcells):
        cell = cells[i].text
        celldata.append(cell)
        print(cell)
    return celldata


get_table(driver)