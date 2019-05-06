import json
import time
from decimal import Decimal
from selenium.webdriver.support import expected_conditions as EC

from django.http import HttpResponse
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from web_scraping.models import TblConsultancyData, TblMonthlyProgressObjectBased


def get_dropdown_list(browser, select_tag_id):
    select_tag = Select(browser.find_element_by_id(select_tag_id))
    arr_options_el = select_tag.options
    data = []
    for index in range(1, len(arr_options_el)):
        option = arr_options_el[index]
        obj = {'name': option.text, 'value': option.get_attribute('value')}
        data.append(obj)
    return data


def scrap_smdp_data(request):
    url = "https://smdp.punjab.gov.pk/Login.aspx"
    user_name = 'dev.gis.pnd'
    password = 'ferrp'
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get(url)
    browser.find_element_by_id('txtLoginName').send_keys(user_name)
    browser.find_element_by_id('txtPassword').send_keys(password)
    browser.find_element_by_id('btnAuthenticate').click()
    url = "https://smdp.punjab.gov.pk/Layouts/Reports/ADPMontlyProgressSchemeBasedReport.aspx"
    browser.get(url)
    browser = get_page(browser, url)
    projects = get_dropdown_list(browser, 'PlaceHolderMain_ddlSchemeName')
    years = get_dropdown_list(browser, 'PlaceHolderMain_ddlYears')
    # months = get_dropdown_list(browser, 'PlaceHolderMain_ddlMonth')
    months = [{"name": "September", "value": "9"}]
    select_project_name = Select(browser.find_element_by_id('PlaceHolderMain_ddlSchemeName'))
    select_year = Select(browser.find_element_by_id('PlaceHolderMain_ddlYears')).first_selected_option.text
    select_month = Select(browser.find_element_by_id('PlaceHolderMain_ddlMonth'))
    # arr_months = select_month.options
    # arr_options_el = select_project_name.options
    for month in months:
        month_name = month.get('name')
        for project in projects:
            project_name = project.get('name')
            gs_no = project_name.split('-')[0].strip()
            select_month.select_by_visible_text(month_name)
            select_project_name.select_by_visible_text(project_name)
            browser.find_element_by_id('PlaceHolderMain_btnShowReport').click()
            wait = WebDriverWait(browser, 120)
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[@cols='21']")))
            table = browser.find_element_by_xpath("//table[@cols='21']")
            time.sleep(5)
            is_saved = save_object_based_scheme_detail(table, gs_no, select_year, month_name, user_name)
            if is_saved:
                browser = get_page(browser, url)
                select_project_name = Select(browser.find_element_by_id('PlaceHolderMain_ddlSchemeName'))
                select_month = Select(browser.find_element_by_id('PlaceHolderMain_ddlMonth'))

    browser.implicitly_wait(10)
    browser.quit()
    return HttpResponse('Done. . ')


def get_page(browser, url):
    time.sleep(10)
    browser.get(url)
    wait = WebDriverWait(browser, 120)
    wait.until(EC.element_to_be_clickable((By.ID, 'PlaceHolderMain_btnShowReport')))
    return browser


def save_object_based_scheme_detail(table, gs_no, financial_year, select_month, user_name):
    arr_rows = table.find_elements_by_tag_name('tr')
    data = []
    try:
        for j in range(18, len(arr_rows)):
            arr_td = arr_rows[j].find_elements_by_tag_name('td')
            if not is_int(arr_td[1].text):
                print(arr_td[
                          1].text + ' and break , gs_no: ' + gs_no + ', select_month: ' + select_month + ', financial_year: ' + financial_year)
                break
            row = {'gs_no': gs_no, 'financial_year': financial_year, 'financial_month': select_month, 'user': user_name}
            object_code_title = arr_td[2].text
            object_code = object_code_title.split('-')[0].strip()
            row['sno'] = int(arr_td[1].text)
            row['object_code'] = object_code
            row['object_code_title'] = arr_td[2].text
            row['provision_total'] = Decimal(arr_td[3].text)
            row['provision_capital'] = arr_td[4].text
            row['provision_revenue'] = arr_td[5].text
            row['revised_allocation_total'] = arr_td[6].text
            row['revised_allocation_capital'] = arr_td[7].text
            row['revised_allocation_revenue'] = arr_td[8].text
            row['pnd_released_total'] = arr_td[9].text
            row['pnd_released_capital'] = arr_td[10].text
            row['pnd_released_revenue'] = arr_td[11].text
            row['fd_released_total'] = arr_td[12].text
            row['fd_released_capital'] = arr_td[13].text
            row['fd_released_revenue'] = arr_td[14].text
            row['received_released_total'] = arr_td[15].text
            row['received_released_capital'] = arr_td[16].text
            row['received_released_revenue'] = arr_td[17].text
            row['utilized'] = arr_td[18].text
            row['percentage_util_revised_allocation'] = arr_td[19].text
            obj_mp = TblMonthlyProgressObjectBased.objects.filter(gs_no=gs_no, financial_year=financial_year,
                                                                  financial_month=select_month, object_code=object_code)
            if obj_mp.count() == 0:
                obj = TblMonthlyProgressObjectBased(**row)
                obj.save(force_insert=True)
            else:
                obj_mp.update(**row)
            data.append(row)
    except Exception as e:
        print(str(e) + ', gs_no: ' + gs_no + ', select_month: ' + select_month + ', financial_year: ' + financial_year)
    return True


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def scrap_ppra_data(request):
    url = "https://eproc.punjab.gov.pk/ActiveTenders.aspx"
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get(url)
    no_of_pages = browser.find_element_by_class_name('rgNumPart').find_elements_by_tag_name('a')
    for i in range(len(no_of_pages)):
        no_of_pages[i].click()
        no_of_pages = browser.find_element_by_class_name('rgNumPart').find_elements_by_tag_name('a')
        rows = browser.find_elements_by_xpath("//*[@class='rgRow' or @class='rgAltRow']")
        save_rows_in_db(i, rows)
    browser.implicitly_wait(10)
    browser.quit()
    return HttpResponse('Done. . ')


def save_rows_in_db(page_no, rows):
    for r in rows:
        tds = r.find_elements_by_tag_name("td")
        row_id = r.get_attribute('id') + '_page' + str(page_no + 1)
        row = {}
        row['procurement_title'] = tds[0].text
        row['procurement_name'] = tds[1].text
        row['type'] = tds[2].text
        row['publish_date'] = tds[3].text
        row['close_date'] = tds[4].text
        row['department'] = tds[5].text
        row['status'] = tds[6].text
        row['tender_notice'] = tds[7].find_element_by_tag_name('a').get_attribute('href')
        row['bidding_document'] = tds[8].find_element_by_tag_name('a').get_attribute('href')
        row['page_no'] = page_no + 1
        row['row_id'] = row_id
        obj_cd = TblConsultancyData.objects.filter(row_id=row_id)
        if obj_cd.count() == 0:
            obj = TblConsultancyData(**row)
            obj.save(force_insert=True)
        else:
            obj_cd.update(**row)
