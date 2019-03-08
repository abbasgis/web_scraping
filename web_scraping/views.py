from django.http import HttpResponse
from selenium import webdriver

from web_scraping.models import TblConsultancyData


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
    print('working')
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
