from selenium import webdriver
from bs4 import BeautifulSoup
import os,random,sys,time
import keyboard
import pandas as pd

path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
wd = webdriver.Chrome(path, options=options)

username = 'tausifiqbal10@gmail.com'
password = 'mechanical.18'

# wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
login_link = 'https://www.linkedin.com/uas/login'
wd.get(login_link)
elementID = wd.find_element_by_id('username')
elementID.send_keys(username)
elementID = wd.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()

visit_profile_id = 'genesisai/'
linkedIn_url = 'https://www.linkedin.com/company/' + visit_profile_id
wd.get(linkedIn_url)

followers_path = 'org-top-card-summary-info-list__info-item'
employees_on_linkenin = 'ember47'


linkedin_data = {}
followers = wd.find_elements_by_class_name(followers_path)
employees_on_link = wd.find_elements_by_id(employees_on_linkenin)

# print(len(followers))
# print(len(employees_on_link))
print(followers[2].text)
print(employees_on_link[0].text[8:20])
linkedin_data['followers'] = followers[2].text
linkedin_data['emplyoees on linkenIn'] = employees_on_link[0].text[8:20]

about_url = 'https://www.linkedin.com/company/'+visit_profile_id+'about/'
wd.get(about_url)
scroll_time = 5

last_height = wd.execute_script("return document.body.scrollHeight")

for i in range(3):
    wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(scroll_time)
    new_height = wd.execute_script("return document.body.scrollHeight")
    if new_height==last_height:
        break
    last_height = new_height

src = wd.page_source
soup = BeautifulSoup(src, 'lxml')

name_div = soup.find('dl', {'class': 'overflow-hidden'})
data_loc = name_div.find_all('dd')
data_get = name_div.find_all('dt')

names = []
datas = []
for i,j in zip(data_loc,data_get):
    names.append(j.get_text().strip())
    if 'LinkedIn' not in i.get_text().strip():
        datas.append(i.get_text().strip())
for i,j in zip(names,datas):
    linkedin_data[i] = j

print(linkedin_data)
linkedin_df = pd.DataFrame(linkedin_data, index=[1])
linkedin_df.to_csv('linkedIndata.csv')
# wd.quit()