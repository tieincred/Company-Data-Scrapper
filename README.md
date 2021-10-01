# DATA SCRAPER FOR COMPANIES

The Project is used to get data for any company from following websites:
Twitter
FaceBook
LinkedIn
Crunchbase

**Pre-Requisites to run the application**
1. You need an python IDE (Recomended: VScode and PyCharm ) 
   
   `Here is the link for VScode download : https://code.visualstudio.com/download`
   
   `Here is the link for Pycharm download : _https://www.jetbrains.com/pycharm/_`
   
   VS code would be better as it's lighter and python extension can be easily installed.
  2. You would need the Chrome driver which works for your version
        
       `Here  is the link to download driver : _https://chromedriver.chromium.org/downloads_`
       
       Note : The application already has a driver for chrome version 94.
       You'll have to check you version and download the driver accordingly.
       
       `Tutorial link to check your chrome version : https://help.zenplanner.com/hc/en-us/articles/204253654-How-to-Find-Your-Internet-Browser-Version-Number-Google-Chrome`
       
       It is necessary to use chrome and no other browser.
       
   3. You need to have a twitter developer profile and should have secret keys of your own.
   
         `Apply for acess using the following link : https://developer.twitter.com/en/apply-for-access`
         
         `Tutorial to get your secret acess keys : https://youtu.be/gLZE1L8UfqA`
         
         Note : Save the keys they'll be used later on.
         
  4. You need a LinkedIn account and should have username and password.
  (Can be easily created on LinkedIn platform)
  
  
 **How to run**
 
 1. In the details.txt file update following credentials:
      
      `consumer_key`
      `consumer_secret`
      `access_token`
      `access_token_secret`
      
      `LinkedIn_username`
      `LinkedIn_Password`
    
    You would get these information from pre-requisites.
 2. In file search_deatils.txt update the following details:
 
     `twitter_username,crunchbase_username,linkedin_username`
     
     These are the username of company you want to search about in different platforms.
     
 3. Now run the file named Scrape_Company_Data.py (How to run a file can be seen in images below) by opening up the file in VS code:
    
    `Note : Make sure python extension is installed VScode keeps suggesting that in bottom right corner and also a play buttton on the top right corner can run the code.` 
    
    
**Results**

After successful Run of the application there would be 3 files generated in the same folder.

`linkedIndata.csv, crunchbase.csv, Data_info.csv`

As name suggests they will have data for linkedIn, Crunchbase and all website data respectively.
The data Include following points:
 1. From LinkedIn: `followers,emplyoees on linkenIn,Website,Industry,Company size,Headquarters,Type,Founded.`
 2. From Twitter: `favourites_count, name, location, friends_count, followers_count, created_at, statuses_count.`
 3. From CrunchBase: `About, address, No. of Employees, Last funding type, IPO status, website,
                   CB rank (company)`
 4. From Facebook : `Followers, likes`
 
Note : The data may change as many company provide more or less data depending upon size and industry.

If you face problem in adding extension and running follow images and instruction below:


FOR PYCHARM :
Right click after opening the file and click on the hihgligted option which say 'run Scrape_Company_Data.py'
![alt text](https://github.com/tieincred/Company-Data-Scrapper/blob/main/Annotation.jpg?raw=true)
