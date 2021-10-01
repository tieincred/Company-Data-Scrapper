from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import pandas as pd
import re
import requests
import Scrape_Company_Data

node = Scrape_Company_Data()

#
path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
wd = webdriver.Chrome(path, options=options)

wd = webdriver.Chrome('chromedriver',chrome_options=options)  #//*[@id="oIjXfBTcVCnEKBo"]
wd.get('https://www.crunchbase.com/organization/genesisai')
time.sleep(5)
# by_pass = (wd.find_elements_by_tag_name('div'))
# for cards in by_pass:
#      checkstr = 'This may happen as a result of the following:'
#      if checkstr in (cards.text):
#          keyboard.press_and_release('tab')
#          keyboard.press('enter')
#          time.sleep(4)
#          keyboard.release('enter')


html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
time.sleep(5)
xpath1 = "/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[1]/profile-section/section-card/mat-card/div[2]/div"
xpath2 = '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[2]/profile-section/section-card/mat-card'
xpath3 = "/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[3]/profile-section/section-card/mat-card"
# icons = "/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[1]/profile-section/section-card/mat-card/div[2]/div/fields-card/ul/li"
# icons_ele = (wd.find_elements_by_xpath(icons))
elements1 = (wd.find_elements_by_xpath(xpath1))
elements2 = (wd.find_elements_by_xpath(xpath2))
elements3 = (wd.find_elements_by_xpath(xpath3))
elements = [elements1, elements2, elements3]
date = []
for element in elements:
    det = []
    for cards in element:
        det.append(cards.text)
    date.append(det)
# for i in date:
#     print(i)

# len_data = soup.find_all('span')
# for i in len_data:
#     if 'GenesisAI' in (i.text).upper():
#         print(i.text)
wd.quit()

new_wd = webdriver.Chrome('chromedriver',chrome_options=options)
new_wd.get('https://www.crunchbase.com/organization/genesisai/technology')
tech_path = '/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[1]/profile-section/section-card/mat-card/div[2]/div/anchored-values/div'
tech_elements = (new_wd.find_elements_by_xpath(tech_path))

tech_data = []
for cards in tech_elements:
    tech_data.append(cards.text)
print('Tech Data:')
print(tech_data)

for d in tech_data:
    date[1].append(d)
print('Tech data appended:')
print(date[1])

for details1,details2,details3 in zip(date[0],date[1],date[2]):
  detail1 = details1.split('\n')
  detail2 = details2.split('\n')
  detail3 = details3.split('\n')

for d in tech_data:
    for i in d.split('\n'):
        detail2.append(i)
print('Check:')
print(detail2)
about = {}
labels1 = ['About', 'address', 'No. of Employees', 'Last funding type', 'IPO status', 'website', 'CB rank (company)']
for data,label in zip(detail1,labels1):
  about[label] = data

detail2.remove('Highlights')
i = 0
for j in range(int(len(detail2)/2)):
  # print(detail2[i])
  # print(detail2[i+1])
  about[detail2[i]] = detail2[i+1]
  i = i + 2
# print(about)

final_df = pd.DataFrame(about, index=[1])
final_df.to_csv('crunchbase.csv')
new_wd.quit()