from bs4 import BeautifulSoup
import requests
import pandas as pd


def yellow_pages(company, location):
    """
    Initialize and export Phone Number data from the Yellow Pages; 
    This uses output from the lists created from the HTML parser below
    """
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
    """
    Messy function that combines the 3 lists below, from the HTML
    parser loop. Does the job for now.
    """
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

# Messy Block for Input so Far. Not quite working
amount_input = int(input("How many jobs do you need?: "))
local_input = input("Which town?: ")
state_input = input("State?: ")
num_inp = int(1 + amount_input)
page_range = int(float(num_inp)*0.2)+1

# These 3 lists are combined below into a Panda DataFrame
company = []
local = []
title = []
# For loop that parses the HTML page from Jora 
for page in range(1, page_range):
    r = requests.get(f'https://au.jora.com/j?l={local_input}+{state_input}&p={page}')
    soup = BeautifulSoup(r.content, 'lxml')
    jobs = soup.find('div', class_="jobresults").find_all('article')
    for index, job in enumerate(jobs):
        index += 1
        print(index)
        if index <= amount_input:
            try:
                company += job.find('span', class_='job-company').get_text().split('\n')
                local += job.find('span', class_='job-location').get_text().split('\n')
                title += job.find('h3', class_='job-title').get_text().split('\n')
            except:
                pass
        else:
            break
#        r = requests.get(f'https://au.jora.com/j?sp=homepage&q=&l={local_input}+{state_input}')
#        soup = BeautifulSoup(r.content, 'lxml')
#        jobs = soup.find('div', class_="jobresults").find_all('article')
#        for index, job in enumerate(jobs):
#            if index <= amount_input:
#                try:
#                    company += job.find('span', class_='job-company').get_text().split('\n')
#                    local += job.find('span', class_='job-location').get_text().split('\n')
#                    title += job.find('h3', class_='job-title').get_text().split('\n')
#                except:
#                    pass



print(len(company))
# Loop that uses the Yellow pages function in order to pull the phone numbers
phone_nums = []
for index, companies in enumerate(company): 
    index += 1
    print(index)
    if index <= amount_input:
        phone_nums += yellow_pages(companies, 'Maryborough').split()
    else:
         break
 


merged_jobs = merge(company, local, title)
df = pd.DataFrame(merged_jobs, columns=['Company', 'Location', 'Title'])
df.apply(lambda col: col.drop_duplicates().reset_index(drop=True) )

print(df) 
phone_nums = list(zip(*[iter(phone_nums)]*3))
res = [' '.join(tups) for tups in phone_nums]
df['Phone Nums'] = pd.Series(res)

print(df)
gfg_csv_data = df.to_csv('Jobs.csv', index = False)
print('\nCSV String:\n', gfg_csv_data)
