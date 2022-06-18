from bs4 import BeautifulSoup
import requests


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


r = requests.get("https://au.jora.com/j?sp=homepage&q=&l=Maryborough+QLD")
soup = BeautifulSoup(r.content, 'lxml')

company = []
local = []
title = []
jobs = soup.find('div', class_="jobresults").find_all('article')
for job in jobs:
    try:
        company += job.find('span', class_='job-company').get_text().split('\n')
        local += job.find('span', class_='job-location').get_text().split('\n')
        title += job.find('h3', class_='job-title').get_text().split('\n')
    except:
        pass


print(merge(company, local, title))

# print(jobs.get_text())
