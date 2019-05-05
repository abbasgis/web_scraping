from django.http import HttpResponse
from django.test import Client
from selenium import webdriver
from selenium.webdriver.support.select import Select

from web_scraping.models import TblConsultancyData


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
    select_project_name = Select(browser.find_element_by_id('PlaceHolderMain_ddlSchemeName'))
    select_year = Select(browser.find_element_by_id('PlaceHolderMain_ddlYears')).first_selected_option.text
    select_month = Select(browser.find_element_by_id('PlaceHolderMain_ddlMonth'))
    arr_months = select_month.options
    arr_options_el = select_project_name.options
    for month in arr_months:
        for i in range(1, len(arr_options_el)):
            gs_no = arr_options_el[i].get_attribute('value')
            project_name = arr_options_el[i].text
            select_month.select_by_visible_text(month)
            select_project_name.select_by_visible_text(project_name)
            browser.find_element_by_id('PlaceHolderMain_btnShowReport').click()
            table = browser.find_element_by_xpath("//table[@cols='21']")
            save_object_based_scheme_detail(table, gs_no, select_year, month, user_name)
            browser = get_page(browser, url)
            select_project_name = Select(browser.find_element_by_id('PlaceHolderMain_ddlSchemeName'))
            arr_options_el = select_project_name.options

    browser.implicitly_wait(10)
    browser.quit()
    return HttpResponse('Done. . ')


def get_page(browser, url):
    browser.get(url)
    return browser


def save_object_based_scheme_detail(table, gs_no, select_year, select_month, user_name):
    arr_rows = table.find_elements_by_tag_name('tr')
    data = []
    for j in range(18, len(arr_rows)):
        arr_td = arr_rows[j].find_elements_by_tag_name('td')
        row = {'gs_no': gs_no, 'financial_year': select_year, 'financial_month': select_month, 'user': user_name}
        row['sno'] = arr_td[1].text
        object_code_title = arr_td[2].text
        provision_total = arr_td[3].text
        provision_capital = arr_td[4].text
        provision_revenue = arr_td[5].text
        revised_allocation_total = arr_td[6].text
        revised_allocation_capital = arr_td[7].text
        revised_allocation_revenue = arr_td[8].text
        pnd_released_total = arr_td[9].text
        pnd_released_capital = arr_td[10].text
        pnd_released_revenue = arr_td[11].text
        fd_released_total = arr_td[12].text
        fd_released_capital = arr_td[13].text
        fd_released_revenue = arr_td[14].text
        received_released_total = arr_td[15].text
        received_released_capital = arr_td[16].text
        received_released_revenue = arr_td[17].text
        utilized = arr_td[18].text
        percentage_util_revised_allocation = arr_td[19].text
        # obj_cd = TblConsultancyData.objects.filter(row_id=row_id)
        # if obj_cd.count() == 0:
        #     obj = TblConsultancyData(**row)
        #     obj.save(force_insert=True)
        # else:
        #     obj_cd.update(**row)
        data.append(row)

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
