from bs4 import BeautifulSoup
import requests
import pandas as pd


def yellow_pages(company, location):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.utils import ChromeType

    from bs4 import BeautifulSoup

    # Setup
    CHROMEDRIVER_PATH = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install() 
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver.get('https://www.yellowpages.com.au/')

    # Bot Time
    search = driver.find_element_by_id("clue")
    search_local = driver.find_element_by_id("where")
    search.send_keys(company)
    search_local.send_keys(location)
    search.send_keys(Keys.RETURN)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    button = soup.find('div', class_='Box__Div-sc-dws99b-0 cINsGc').find('button', class_='MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-fullWidth')
    return button.get_text()

    driver.close()


def merge(list1, list2, list3):
    merged_list = []
    for i in range(max((len(list1), len(list2), len(list3)))):
        while True:
            try:
                tup = (list1[i], list2[i], list3[i])
            except IndexError:
                if len(list1) > len(list2):
                    list2.append('')
                    tup = (list1[i]. list2[i], list3[i])

                elif len(list1) < len(list2):
                    list1.append('')
                    tup = (list1[i], list2[i], list3[i])

                elif len(list3) < len(list2):
                    list3.append('')
                    tup = (list1[i], list2[i], list3[i])

                elif len(list3) > len(list2):
                    list2.append('')
                    tup = (list1[i], list2[i], list3[i])

                elif len(list3) < len(list1):
                    list3.append('')
                    tup = (list1[i], list2[i], list3[i])

                elif len(list3) > len(list2):
                    list2.append('')
                    tup = (list1[i], list2[i], list3[i])
                continue
            merged_list.append(tup)
            break
    return merged_list

company = []
local = []
title = []
for page in range(1):
    r = requests.get(f'https://au.jora.com/j?l=Maryborough+QLD&p={page}')
    soup = BeautifulSoup(r.content, 'lxml')

    jobs = soup.find('div', class_="jobresults").find_all('article')
    for index, job in enumerate(jobs):
        if index <= 3:
            try:
                company += job.find('span', class_='job-company').get_text().split('\n')
                local += job.find('span', class_='job-location').get_text().split('\n')
                title += job.find('h3', class_='job-title').get_text().split('\n')
            except:
                pass

phone_nums = []
for index, companies in enumerate(company):
    if index <= 3:
        phone_nums += yellow_pages(companies, 'Maryborough').split()
    else:
        break
        



merged_jobs = merge(company, local, title)
df = pd.DataFrame(merged_jobs, columns=['Company', 'Location', 'Title'])

print(df) 
phone_nums = list(zip(*[iter(phone_nums)]*3))
res = [' '.join(tups) for tups in phone_nums]
df['Phone Nums'] = res
print(df)
gfg_csv_data = df.to_csv('Jobs.csv', index = False)
print('\nCSV String:\n', gfg_csv_data)
