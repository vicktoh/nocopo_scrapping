import json
import atexit
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from element_has_changed import element_has_changed

def __main():
    driver = webdriver.Chrome()
    driver.implicitly_wait(7)
    base_path = "https://nocopo.bpp.gov.ng/noc/frmCitizenDashBoard.aspx"
    driver.get(base_path)
    get_count(driver)
    # reversed()
    # get_det_pages(driver)
def reversed():
    file = json.loads(open("memoized.json").read())
    newmodized = {}
    for m in file:
        newmodized[file[m]] = True
    data = json.dumps(newmodized);
    filehanlde = open("anothermemo.json", "w")
    filehanlde.write(data)
    print('Memoized')
def get_det_pages(driver):
    mdas = json.loads(open("newmemoised.json").read())
    start  = 20
    ministries = json.loads(open("ministrylist.json").read())
    for i in range(start, len(ministries)):
        checkbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxAdvancedSearch")
        checkbox.click()
        #wait for the checkbox form to show
        element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Panel1"))
        )
        #find the ministry dropdown
        minstryCheckbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxMinistry")
        minstryCheckbox.click()
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboMinistry"))
        )
        ministry_dropdown = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboMinistry"))
        ministry_dropdown.select_by_value(ministries[i])
        #select pe
        pe =  driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxProcuringEntities")
        pe.click();
        #wait for it to become active
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboProcuringEntities"))
        )
        procureSelect = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboProcuringEntities")
        procuringEntities = procureSelect.find_elements_by_css_selector("option")
        for opt in procuringEntities:
            
            if(opt.text in mdas):
                print("found %s"%opt.text)
                mdas[opt.text] = ministries[i]
            
        
        data = json.dumps(mdas)
        filereader = open('newmemoised.json', 'w')
        filereader.write(data)
        print("finisth page %s"%i)
        driver.refresh()
def get_count(driver):
 
    count_obj = json.loads(open("counts.json").read())
    
    mdas = json.loads(open("newmemoised.json", 'r').read())
    for mda in mdas:
        mda_obj = {}
        parastatal = mdas[mda]
        if(not parastatal):
            continue
        if(mda in count_obj):
            continue
        #select the checkbox to search
        checkbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxAdvancedSearch")
        checkbox.click()
        #wait for the checkbox form to show
        element = WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Panel1"))
        )
         #find the ministry dropdown
        minstryCheckbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxMinistry")
        minstryCheckbox.click()
        #wait until list shows
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboMinistry"))
        )
        #select parent ministry 
        select = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboMinistry"))
        select.select_by_value(parastatal)
        #select the procuring entity
        pe =  driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxProcuringEntities")
        pe.click();
        #wait for it to become active
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboProcuringEntities"))
        )
        #select MDA;
        peselect = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboProcuringEntities"))
        peselect.select_by_value(mda)

        #budgetYear button 
        #find the 20202 checkbox
        checkbox2020 = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxBudgetYear")
        checkbox2020.click()
        #budgetYear
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboBoxBudgetYear"))
        )
        #select Year
        yearSelect = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboBoxBudgetYear"))
        yearSelect.select_by_value("2019")
        counter = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCount")
        
        #click search
        search_button = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonSearch")
        search_button.click()
        #waitfor result
        element = WebDriverWait(driver, 15).until(
            element_has_changed((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCount"), driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCount").text)
        )

        #record count;
        count = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCount")
        print(count.text)
        mda_obj['2019'] = count.text
        Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboBoxBudgetYear")).select_by_value("2020")

        #click search
        search_button = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonSearch")
        search_button.click()
        #waitfor result
        element = WebDriverWait(driver, 15).until(
            element_has_changed((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCount"), count.text)
        )
        count = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCount")
        mda_obj['2020'] = count.text

        count_obj[mda] = mda_obj
        data = json.dumps(count_obj)
        filereader = open('counts.json', 'w')
        filereader.write(data)
        print("finisth mda %s"%mda)
        driver.refresh()    

def select_2019_option(driver):
        #select the checkbox to search
        checkbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxAdvancedSearch")
        checkbox.click()
        #wait for the checkbox form to show
        element = WebDriverWait(driver, 15).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Panel1"))
        )
        #find the ministry dropdown
        minstryCheckbox = driver.find_element_by_css_selector("#ctl00$ContentPlaceHolder1$comboMinistry");
        
        #find the 2020 checkbox
        checkbox2020 = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxBudgetYear")
        checkbox2020.click()
        #wait until 
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboBoxBudgetYear"))
        )
        #wait until
        select = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboBoxBudgetYear"))
        select.select_by_value("2019")
        #click the searchbutton
        search_button = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonSearch")
        search_button.click()
        #wait for loaded results
        element = WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCount"), "3669" )
        )

def get_all_the_ministries(driver):
    ministries = []
    checkbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxAdvancedSearch")
    checkbox.click()
    #wait for the checkbox form to show
    element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Panel1"))
    )
    #find the ministry dropdown
    minstryCheckbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxMinistry")
    minstryCheckbox.click()
    element = WebDriverWait(driver, 15).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboMinistry"))
    )

    select = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_comboMinistry")
    options =  select.find_elements_by_css_selector("option")
    for opt in options:
        ministries.append(opt.text)

    ministry_json = json.dumps(ministries)
    filehandle = open('ministrylist.json', 'w')
    filehandle.write(ministry_json)
    print("We are done heare")

__main()