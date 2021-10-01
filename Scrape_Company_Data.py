from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import pandas as pd
import re
import requests
import tweepy as tw
from twython import Twython

class ScrapeCompanyData:
    def __init__(self, twitter_name,crunchbase_name,linkedin_name):
        self.consumer_key = 'AdW0DwnyMprbY8jPCQBT6wOi0'
        self.consumer_secret = 'z9Uq6O8uW60CN70phXrsWHDGgU4zx5Ex1tfKtSfiaGPItXcbp4'
        self.access_token = '1394308063595614217-tjHbbYsIvoKzdWgljbjnziaMwjxq1l'
        self.access_token_secret = '4FNiCSu2dgRMpW8P0iR94vGS2EhsxhYfNNyW8V4LbgpRU'
        self.tweet = twitter_name
        self.crunch = crunchbase_name
        self.link = linkedin_name
        self.username = 'tausifiqbal10@gmail.com'
        self.password = 'mechanical.18'

    def update_linkedin_cred(self, username, password):
        self.username = username
        self.password = password


    def update_tweetkeys(self,consumer_key,consumer_secret,access_token,access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret


    def authorise_tweet(self):
        auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tw.API(auth)
        return api

    def get_tweeter_data(self, latest_tweet=False):
        api = self.authorise_tweet()
        twitter = Twython(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)

        details = twitter.show_user(screen_name=self.tweet)
        extracted = {}
        info = ['favourites_count', 'name', 'location', 'friends_count', 'followers_count', 'created_at',
                'statuses_count']
        for data in info:
            extracted[data] = details[data]
        tweets = []
        tweeted_at = []

        for i in tw.Cursor(api.search, q='from:' + self.tweet, tweet_mode='extended').items(10):
            tweets.append(i.full_text)
            tweeted_at.append(i.created_at)
        # extracted['latest_tweet_on'] = tweeted_at[0]
        print(tweeted_at)

        import datetime
        s = details['created_at'][:10] + details['created_at'][25:]
        d = datetime.datetime.strptime(s, '%a %b %d %Y')

        extracted['days_per_tweet'] = round(((datetime.datetime.now() - d).days) / details['statuses_count'])

        if latest_tweet:
            return tweets[0], pd.DataFrame(extracted, index=[1])
        else:
            return pd.DataFrame(extracted, index=[1])


    def get_linkedin_data(self):
        path = 'chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        wd = webdriver.Chrome(path, options=options)


        # wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
        login_link = 'https://www.linkedin.com/uas/login'
        wd.get(login_link)
        elementID = wd.find_element_by_id('username')
        elementID.send_keys(self.username)
        elementID = wd.find_element_by_id('password')
        elementID.send_keys(self.password)
        elementID.submit()

        visit_profile_id = self.link+'/'
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

        about_url = 'https://www.linkedin.com/company/' + visit_profile_id + 'about/'
        wd.get(about_url)
        scroll_time = 5

        last_height = wd.execute_script("return document.body.scrollHeight")

        for i in range(3):
            wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(scroll_time)
            new_height = wd.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        src = wd.page_source
        soup = BeautifulSoup(src, 'lxml')

        name_div = soup.find('dl', {'class': 'overflow-hidden'})
        data_loc = name_div.find_all('dd')
        data_get = name_div.find_all('dt')

        names = []
        datas = []
        for i, j in zip(data_loc, data_get):
            names.append(j.get_text().strip())
            if 'LinkedIn' not in i.get_text().strip():
                datas.append(i.get_text().strip())
        for i, j in zip(names, datas):
            linkedin_data[i] = j

        print(linkedin_data)
        linkedin_df = pd.DataFrame(linkedin_data, index=[1])
        linkedin_df.to_csv('linkedIndata.csv')
        wd.quit()
        return linkedin_df


    def get_crunchbase_data(self):
        path = 'chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        wd = webdriver.Chrome(path, options=options)

        wd = webdriver.Chrome('chromedriver', chrome_options=options)  # //*[@id="oIjXfBTcVCnEKBo"]
        wd.get('https://www.crunchbase.com/organization/'+self.crunch)
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

        new_wd = webdriver.Chrome('chromedriver', chrome_options=options)
        new_wd.get('https://www.crunchbase.com/organization/'+self.crunch+'/technology')
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

        for details1, details2, details3 in zip(date[0], date[1], date[2]):
            detail1 = details1.split('\n')
            detail2 = details2.split('\n')
            detail3 = details3.split('\n')

        for d in tech_data:
            for i in d.split('\n'):
                detail2.append(i)
        print('Check:')
        print(detail2)
        about = {}
        labels1 = ['About', 'address', 'No. of Employees', 'Last funding type', 'IPO status', 'website',
                   'CB rank (company)']
        for data, label in zip(detail1, labels1):
            about[label] = data

        detail2.remove('Highlights')
        i = 0
        for j in range(int(len(detail2) / 2)):
            # print(detail2[i])
            # print(detail2[i+1])
            about[detail2[i]] = detail2[i + 1]
            i = i + 2
        # print(about)

        final_df = pd.DataFrame(about, index=[1])
        final_df.to_csv('crunchbase.csv')
        new_wd.quit()
        return final_df

if __name__ == '__main__':
    start = ScrapeCompanyData('miniOrange_Inc','miniorange','miniorange-incorporated')
    data1 = start.get_crunchbase_data()
    data2 = start.get_linkedin_data()
    data3 = start.get_tweeter_data()
    for col in data2.columns:
        data1[col] = data2[col]
    for col in data3.columns:
        data1[col] = data3[col]
    data1.to_csv('Data_info.csv')