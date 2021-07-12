from os import path
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    """
    Base representation of a page
    """
    def __init__ (self, driver):
        self.driver = driver
        if (path.exists('2020tabledata.json')):
            file = open('2020tabledata.json', 'r')
            table_data = json.loads(file.read())
            self.data_dict = table_data
        else:
            self.data_dict = {}
        if (path.exists('details.json')):
            detailfile = open('details.json', 'r')
            details_obj = json.loads(detailfile.read())
            self.details_dict = details_obj
        else:
            self.details_dict = {}

        if (path.exists('meta.json')):
            metafile = open('meta.json', 'r')
            meta_obj = json.loads(metafile.read())
            self.meta = meta_obj
        else:
            self.meta = {"page" : 1, "row" : 1}




class DataPage(object):
    def __init__ (self, driver):
        self.driver = driver

    def fetch_page_data (self):
        tables = {"planning": "GridViewPlanningDetails", "tender": "GridViewTenderDetails", "award": "GridViewAwardDetails", "contract":"GridViewCOntractDetails", "implementation": "GridViewIMplementationDetails"}
        pagedata = {}
        for stage in tables:
            pagedata[stage] = self.fetch_elements_from_page(tables[stage])
        
        print(pagedata)
        return pagedata
    def fetch_elements_from_page (self, element_id):
        obj = {}
        count = 1
        path = 'table#'+element_id + " tbody"
        tbody = self.driver.find_element_by_css_selector(path)
        elements = tbody.find_elements_by_tag_name('tr')
        for tr in elements:
            if count == 1:
                count+=1
                continue
            key = tr.find_element_by_css_selector('td:nth-child(1)').text
            value = tr.find_element_by_css_selector('td:nth-child(2)').text
            obj[key] = value
            count += 1
        return obj


class TablePage(BasePage):
    def select_2020_option(self):
        #select the checkbox to search
        checkbox = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxAdvancedSearch")
        checkbox.click()
        #wait for the checkbox form to show
        element = WebDriverWait(self.driver, 25).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_Panel1"))
        )
        #find the 20202 checkbox
        checkbox2020 = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_CheckBoxBudgetYear")
        checkbox2020.click()
        #wait until 
        element = WebDriverWait(self.driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_comboBoxBudgetYear"))
        )
        #click the searchbutton
        search_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonSearch")
        search_button.click()
        #wait for loaded results
        element = WebDriverWait(self.driver, 25).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCount"), "7502")
        )
    def table_data(self):
        pages_element = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblTotalPages")
        next_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonNextPage")
        pages = int(pages_element.text)
        DetailsPage = DataPage(self.driver)
        current_page_element = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCurrentPage")
        current_page = int(current_page_element.text)
        curr_page = self.meta['page']
        while (curr_page != current_page and current_page < curr_page):
            next_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonNextPage")
            next_button.click()
            nxt_page = str(curr_page)
            print(nxt_page)
            element = WebDriverWait(self.driver, 10).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCurrentPage"), str(curr_page))
                )
            current_page_element = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCurrentPage")
            current_page = int(current_page_element.text)
            curr_page = self.meta['page']
            
        current_row = self.meta['row']
        print(pages)
        for i in range(current_page, pages):
                
            rows  =  self.driver.find_elements_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2 > tbody > tr")
            self.meta["page"] = i
            num_rows = len(rows)
            for j in range(current_row,num_rows):
                self.meta["row"] = j
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_GridViewProjectLIst2 > tbody > tr:nth-child(%s)"%j))
                )
                row =self.driver.find_elements_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2 > tbody > tr")[j]
                print(row.text)
                select = row.find_element_by_tag_name("input")
                ctl = str(j+1).zfill(2)
                ocid = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblOCID2"%ctl).text
                title = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblProjectTitle2"%ctl).text
                mda = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblMDA2"%ctl).text
                budget_amount = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblBudgetAmount2"%ctl).text
                year = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblBudgetYear2"%ctl).text
                contract_amount = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblCOntractValue2"%ctl).text
                contractor = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblContractor2"%ctl).text
                stage = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblProcurementStatus2"%ctl).text
                status = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblProjectStatus"%ctl).text
                self.data_dict[ocid] = { "ocid": ocid, "title": title, "mda": mda, "budget_amount": budget_amount, "year":year, "contract_amount": contract_amount, "contractor": contractor, "stage": stage, "status": status}
                #entering details page
                select.click()
                print_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonPrint")
                print_button.click()
                #fetching the details of the project
                details = DetailsPage.fetch_page_data()
                self.details_dict[ocid] = details
                back_button = self.driver.find_element_by_css_selector("input[name=ButtonBack]")
                back_button.click()
                #back to details page
                back_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonBack")
                back_button.click()
                #back to table_page
                print("finished row {j} on page {i}")
            print("finished page {i} going to next")
            next_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonNextPage")
            next_button.click()
            nextpage = str(i + 1)
            element = WebDriverWait(self.driver, 10).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCurrentPage"), nextpage)
                )
            self.meta['row'] = 1
        return (self.data_dict, self.details_dict)
    def cleanup(self):
        details_file = open('details.json', 'w')
        data_file = open('2020tabledata.json', 'w')
        meta_file = open('meta.json', 'w')

        details_json = json.dumps(self.details_dict)
        details_file.write(details_json)

        data_json = json.dumps(self.data_dict)
        data_file.write(data_json)

        meta_json = json.dumps(self.meta)
        meta_file.write(meta_json)

        meta_file.close()
        data_file.close()
        details_file.close()
        print('Finished Cleaning up')
    def table_only(self):
        self.select_2020_option()
        pages_element = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblTotalPages")
        next_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonNextPage")
        pages = int(pages_element.text) + 1
        DetailsPage = DataPage(self.driver)
        current_page_element = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCurrentPage")
        current_page = int(current_page_element.text)
        curr_page = self.meta['page']
        while (curr_page != current_page and current_page < curr_page):
            next_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonNextPage")
            next_button.click()
            nxt_page = str(current_page + 1)
            print(nxt_page)
            element = WebDriverWait(self.driver, 25).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCurrentPage"), str(nxt_page))
                )
            current_page_element = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_lblCurrentPage")
            current_page = int(current_page_element.text)
            curr_page = self.meta['page']
            
        
        print(pages)
        for i in range(current_page, pages):
                
            rows  =  self.driver.find_elements_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2 > tbody > tr")
            self.meta["page"] = i
            num_rows = len(rows)
            current_row = self.meta['row']
            for j in range(current_row,num_rows):
                self.meta["row"] = j
                element = WebDriverWait(self.driver, 25).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_GridViewProjectLIst2 > tbody > tr:nth-child(%s)"%j))
                )
                row =self.driver.find_elements_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2 > tbody > tr")[j]
                print(row.text)
                select = row.find_element_by_tag_name("input")
                ctl = str(j+1).zfill(2)
                ocid = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblOCID2"%ctl).text
                title = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblProjectTitle2"%ctl).text
                mda = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblMDA2"%ctl).text
                budget_amount = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblBudgetAmount2"%ctl).text
                year = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblBudgetYear2"%ctl).text
                contract_amount = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblCOntractValue2"%ctl).text
                contractor = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblContractor2"%ctl).text
                stage = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblProcurementStatus2"%ctl).text
                status = row.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_GridViewProjectLIst2_ctl%s_lblProjectStatus"%ctl).text
                self.data_dict[ocid] = { "ocid": ocid, "title": title, "mda": mda, "budget_amount": budget_amount, "year":year, "contract_amount": contract_amount, "contractor": contractor, "stage": stage, "status": status}
            print("finished page {i} going to next")
            self.meta['row'] = 1
            next_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ButtonNextPage")
            next_button.click()
            nextpage = str(i + 1)
            print("nextpage is %s"%nextpage)
            element = WebDriverWait(self.driver, 25).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lblCurrentPage"), nextpage)
                )
            
        return (self.data_dict, self.details_dict)



        



                
         

