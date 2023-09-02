import time 
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service




class TwitterScraper():
    def __init__(self):
        self.result_links = set()
        self.result = set()
        self.set_tweets = set() #link tweet acc
        # PROXY = "116.254.117.162"
        self.option = Options()

        self.option.add_argument("--disable-infobars")
        self.option.add_argument("--disable-extensions")
        self.option.add_argument("USER AGENT")
        # option.add_argument(f'--proxy-server={PROXY}')
        # option.add_argument('--headless')
        # option.add_argument('--no-sandbox')
        # option.add_argument('--disable-setuid-sandbox')
        self.option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2 # 1:allow 2:block 
        })
        # create instance of Chrome webdriver
        self.driver = webdriver.Chrome(executable_path="C:\chromedriver-win64\chromedriver.exe",chrome_options=self.option)
        
        # mozila_service = Service("C:\geckodriver.exe")  # Change to your driver path
        # self.driver = webdriver.Firefox(service=mozila_service)

        # self.driver = webdriver.Edge(executable_path = "C:\\Users\\jmspa\\Downloads\\edgedriver_win64\\msedgedriver.exe")
        self.screen_height=self.driver.execute_script("return window.screen.height;")
        
    def get_result(self):
        return self.result

    #ACCOUNT
    def filter_tweet_date(self,start_date,end_date,id):
        #date format '2022-03-01'
        filter_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        filter_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if id == 1:
            list_tweet = list(self.set_tweets)
        else:
            list_tweet = list(self.result_links)
        set_tweets_filtered = [tweet for tweet in list_tweet if (filter_end_date >= datetime.strptime(tweet[1][:10], '%Y-%m-%d').date() and  datetime.strptime(tweet[1][:10], '%Y-%m-%d').date() >= filter_start_date)]
        return set_tweets_filtered

    def get_info(self,c,links,account):
        try:
            # /div/div/article/div/div/div[2]/div[2]/div[2]/div
            container = c.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]')
            content = container.find_element(By.XPATH,'div[2]/div').text
            content = content.replace('\n',' ')
            # time.sleep(1)
            try:
                emoji = container.find_elements(By.XPATH,'div[2]/div/img') #coba emoji
                for emot in emoji:
                    content+=emot.get_attribute('alt')
            except:
                pass
            name = container.find_element(By.XPATH,'div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span').text
            # print(name)
            comment_time = container.find_element(By.XPATH,'div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time')
            comment_date = datetime.strptime(comment_time.get_attribute('datetime'), "%Y-%m-%dT%H:%M:%S.%fZ").date()
            # date_post = tweet[1]
            # links = tweet[0]
            print(name,';',content,';',comment_date,';','Twitter',';',links,';',account)
            self.result.add((name,content,comment_date,'Twitter',links,account)) #,date_post

        except:
            pass


    def search_by_account(self,account:str,scroll_time:int,start_date:str,end_date:str):
        self.driver.get("https://twitter.com/"+account)
        self.wait()
        i=1
        start=time.time()
        while True:
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=self.screen_height, i=i))
            i += 0.3
            tweets = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div')
                                                        
            # try:
            #     driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]').click()
            # except:
            #     pass

            time.sleep(1)
            for tweet in tweets:
                try:
                    link = tweet.find_element(By.XPATH,"div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a").get_attribute("href")
                    tanggal = tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time').get_attribute("datetime")
                    # tanggal = datetime.strptime(tanggal, "%Y-%m-%dT%H:%M:%S.%fZ").date()
                    # print(tanggal)
                    try:
                        num_reply = int(tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/span/span/span').text)
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[3]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[4]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[2]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[3]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span
                        # /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[4]/div/div/article/div/div/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/span/span/span
                    except:
                        num_reply = 10
                    # tweet_text = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="tweetText"]').text #text postnya jika perlu
                    # print(link, tanggal)
                    print('Jumlah reply = ', num_reply)
                    self.set_tweets.add((link, tanggal,num_reply))
                except:
                    # print('>')
                    pass
            
            end=time.time()
            if round(end-start)>scroll_time: #scroll
                break
        self.scroll_post_comments(start_date,end_date,account)

    def scroll_post_comments(self,start_date,end_date,account):
        set_tweets_filtered = self.filter_tweet_date(start_date,end_date,1)
        # print(set_tweets_filtered)
        for tweet in set_tweets_filtered:
            self.driver.get(tweet[0])
            time.sleep(1)
            num = tweet[2]
            curr_num = 0
            # date_post = tweet[1]
            links = tweet[0]
            while round(curr_num,1) != round((int(num)/10)+2,1):
                time.sleep(2)
                print('Scroll',round(curr_num,1),round((int(num)/10)+2,1))
                screen_height=self.driver.execute_script("return window.screen.height;")

                
                comment = self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div')
                threads = list()
                for j in range(len(comment)):
                    x = Thread(target=self.get_info,args=(comment[j],links,account,)) #,date_post
                    x.start()
                    threads.append(x)

                for index,thread in enumerate(threads):
                    thread.join()

                # time.sleep(1)
                try:
                    more_comment = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[11]/div/div/div').click()
                except:
                    pass

                try:
                    more_comment = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[13]/div/div/article/div/div/div[2]/div/div/div[2]/div').click()
                except:
                    pass
                
                try:
                    view = self.driver.find_element(By.CLASS_NAME,'css-1dbjc4n.r-1ndi9ce').click()
                except:
                    pass

                try:
                    try:
                        view2 = self.driver.find_element(By.CSS_SELECTOR,'div.css-901oao.r-1cvl2hr.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-q4m81j.r-qvutc0').click()
                    except:
                        view2 = self.driver.find_element(By.CSS_SELECTOR,'.r-1pl7oy7 > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').click()
                except:
                    pass
                curr_num += 0.1
                self.driver.execute_script("window.scrollTo(0, {screen_height}*{curr_num});".format(screen_height=screen_height, curr_num=curr_num))
        self.set_tweets = set()
    # KEYWORD
    def search_key_url(self,search,type):
        search = search.replace(" ", "%20")
        search = search.replace("@", "%40")
        search = search.replace("#", "%23")
        if type == 'latest':
            url = f"https://twitter.com/search?q={search}&src=typed_query&f=live"
        else:
            url = f"https://twitter.com/search?q={search}&src=typed_query"
        return url

    def wait(self):
        state = ""
        while state != "complete":
            print("wait for loading to complete")
            time.sleep(randint(3, 5))
            state = self.driver.execute_script("return document.readyState")
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located( 
                (By.CSS_SELECTOR, "a[href*='status']")))
        except WebDriverException:
            print("Tweets did not appear!")
        return True

    def thread_function(self,tweet):
        try:
            user_name = tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span').text
            if user_name != '@BankMegaID':
                # /html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/div/div
                # /html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/div/div[8]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time
                date = tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time').get_attribute("datetime")
                try:
                    link = tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/div/a').get_attribute("href") #pin???
                except:
                    pass
                try:
                    link = tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a').get_attribute("href")
                except:
                    pass
                try:
                    num_comment = tweet.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span').text
                    if 'K' in num_comment:
                        num_comment = num_comment.replace('K', '000')
                        num_comment = num_comment.replace('.', '')
                        num_comment = num_comment.replace(',', '')
                except:
                    num_comment = 0
                self.result_links.add((link,date,num_comment))

        except:
            # print('>')
            pass


    def find_retweets(self,start_date,end_date,account):
        links = self.filter_tweet_date(start_date,end_date,2)
        for link in links:
            tweet_link = list(link)[0]
            self.driver.get(tweet_link)
            try:
                user_name = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span').text
                comments = ''
                try:
                    user_comments = self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[1]/span')
                    for comment in user_comments:
                        comments += comment.text
                except:
                    pass
                try:
                    emoji = self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[1]/img') #coba emoji
                    for emot in emoji:
                        comments+=emot.get_attribute('alt')
                except:
                    pass

                tweet_date = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div/div/div/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time').get_attribute("datetime")
                platform = 'Twitter'
                print(user_name,';',comments,';',tweet_date,';',platform,';',tweet_link,';',account)
                self.result.add((user_name,comments,tweet_date,platform,tweet_link,account))
                num_komen = int(list(link)[2])
                num = (num_komen/10)+1 if num_komen < 100 else 10 #number scroll comment
                i = 0
                while round(i,1)!=round(num,1):
                    # print(round(i,1),round(num,1))
                    self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=self.screen_height, i=i+0.1))
                    i+=0.1
                    komentars = self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div/div/div')
                    threads = list()
                    for komentar in komentars:
                        x = Thread(target=self.find_retweet_comments,args=(komentar,tweet_link,account,))
                        x.start()
                        threads.append(x)
                    for index,thread in enumerate(threads):
                        thread.join()
                    try:
                        more_comment = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[11]/div/div/div').click()
                    except:
                        pass

                    try:
                        more_comment = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[13]/div/div/article/div/div/div[2]/div/div/div[2]/div').click()
                    except:
                        pass
                    
                    try:
                        view = self.driver.find_element(By.CLASS_NAME,'css-1dbjc4n.r-1ndi9ce').click()
                    except:
                        pass

                    try:
                        try:
                            view2 = self.driver.find_element(By.CSS_SELECTOR,'div.css-901oao.r-1cvl2hr.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-q4m81j.r-qvutc0').click()
                        except:
                            view2 = self.driver.find_element(By.CSS_SELECTOR,'.r-1pl7oy7 > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').click()
                    except:
                        pass
            except:
                pass
        self.result_links = set()

    def find_retweet_comments(self,element,link,account):
        try:
            tanggal = element.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time').get_attribute("datetime")
            user = element.find_element(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span').text
            comments = ''
            try:
                user_comments = element.find_elements(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[2]/div/span')
                for comment in user_comments:
                    comments += comment.text
            except:
                pass

            try:
                emoji = element.find_elements(By.XPATH,'div/div/article/div/div/div[2]/div[2]/div[2]/div/img') #coba emoji
                for emot in emoji:
                    comments+=emot.get_attribute('alt')
            except:
                pass
            print(user,';',comments,';',tanggal,';','Twitter',';',link,';',account)
            self.result.add((user,comments,tanggal,'Twitter',link,account))
        except:
            pass

    

    def login(self):
        self.driver.get("https://twitter.com/i/flow/login")
        self.wait()

        self.driver.find_element_by_xpath("//input[@autocomplete='username']").send_keys('joentoro41@students.calvin.ac.id')
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]').click()
        self.wait()

        try:
            self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys('OentoroJam86824')
            self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div').click()
            self.wait()
        except:
            pass


        self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys('Maisie@77')
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()
        self.wait()


    def search_by_keyword(self,keywords:list,mode:list,scroll:int,start_date:str,end_date:str,account:str):
        for j in mode:
            for key in keywords:    
                self.driver.get(self.search_key_url(key,j))
                i=1
                start=time.time()
                threads = list()
                while True:
                    self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=self.screen_height, i=i))
                    tweets = self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/div/div')
                    self.driver.implicitly_wait(1)
                    for tweet in tweets:
                        x = Thread(target=self.thread_function,args=(tweet,))
                        x.start()
                        threads.append(x)
                    for index,thread in enumerate(threads):
                        thread.join()
                    i += 0.2
                    end=time.time()
                    if round(end-start)>scroll: #scroll
                        break
        # print(len(self.result_links))
        self.find_retweets(start_date,end_date,account)

    def save_to_excel(self,file_name):
        df = pd.DataFrame(self.result, columns=['user_name', 'user_comments', 'tweet_date', 'platform','link','bank'])
        print(df)
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='TwitterData', index=False)
        writer.save()
        print('saved')



if __name__ == "__main__":
    # Record the start time
    start_time = time.time()
    scraper = TwitterScraper()
    keywords ={ 'BankMegaID':[
                    'Bank Mega',
                    '@BankMegaID',
                    '@bankmega',
                    '#bankmega',
                    '#BikinJadiSmile',
                    '#SeriusBisa',
                    '#SeriusBisaHealing',
                    '#MeriahBarengMega',
                    '#MegaTravelFair2023',
                    '#MegaSavingHacks',
                    '#MeriahBarengMega2023',
                    '#BantuMegaMinNaikinFollowers',
                    'kartu kredit mega',
                    'kartu kredit bank mega',
                    'Kartu kredit Bank Mega bikin untung',
                    'cc mega',
                    'cc bank mega',
                    'megamin']
                # ],
                # 'BNI':[
                #     'Bank Negara Indonesia',
                #     'BNI', 
                #     '@BNI',
                #     '#BNI',
                #     '#BNI46',
                #     'bni mobile banking',
                #     'tapcash'
                # ],
                # 'BANKBRI_ID':[
                #     'Bank Rakyat Indonesia',
                #     'BRI',
                #     '@BANKBRI_ID',
                #     '#BRI',
                #     'brimo',
                #     '@kontakBRI',
                #     '@promo_BRI',
                #     'BRImo',
                #     '#MemberiMaknaIndonesia'
                # ],
                # 'bankmandiri':[
                #     'Bank Mandiri',
                #     'Mandiri',
                #     '@bankmandiri',
                #     '#bankmandiri',
                #     'livin',
                #     'livin mandiri',
                #     '#TebakanMandiri',
                #     '#livingalivelylife',
                #     '#LivinbyMandiri',
                #     '#mandiripromo'],
                # 'BankBCA':[
                #     'Bank BCA',
                #     'Bank Central Asia',
                #     'BCA',
                #     '@BankBCA',
                #     '#bankbca',
                #     '#bca',
                #     'bca mobile',
                #     '@HaloBCA'
                #     ],
                # 'bankocbcnisp':[
                #     'Bank OCBC',
                #     'Bank OCBC NISP',
                #     '@bankocbcnisp',
                #     '@bankocbc',
                #     '@TanyaOCBCNISP'
                #     ,'ocbc nisp'
                #     ],
                # 'danamon':[
                #     'Bank Danamon',
                #     '@danamon',
                #     'Danamon66',
                #     'Danamon',
                #     '@HelloDanamon',
                #     '#PromoDanamon',
                #     '#SaatnyaPegangKendali'
                #     ],
                # 'CIMBNiaga':[
                #     'CIMB Niaga',
                #     '@CIMBNiaga',
                #     '#CIMBNiaga',
                #     '#CIMBNiaga',
                #     '#BeneranPraktis',
                #     'OCTO Mobile'
                #     ],
                # 'dbsbank':[
                #     'DBS Indonesia',
                #     'Bank DBS Indonesia',
                #     'digibank',
                #     'digibanking',
                #     'digibank by DBS'
                #     ],
                # 'PermataBank':[
                #     'Bank Permata',
                #     '@PermataBank',
                #     '@PermataCare',
                #     '#PermataBank',
                #     '#PermataHati',
                #     '#PermataBankGA'
                #     ],
                # 'SeaBankID':[
                #     'SeaBank Indonesia',
                #     '@SeaBankID',
                #     '#SeaBankID',
                #     '#LebihUntungdiSeaBank',
                #     '#LebihMudahdiSeaBank',
                #     'SIAP #SeaBankID',
                #     'UNTUNG #SeaBankID',
                #     'CUAN #SeaBankID',
                #     'MUDAH #SeaBankID',
                #     '#SobatCuanSobatSeaBank',
                #     'MANTUL #SeaBankID',
                #     'SEABANK #SeaBankID',
                #     'SEABANK',
                #     '#QRISDISEABANK'
                #     ],
                # 'blubybcadigital':[
                #     'Blu BCA',
                #     '@blubybcadigital',
                #     'blubybcadigital',
                #     '@haloblu',
                #     'Blu BCA Digital',
                #     'bluSayangBunda',
                #     'bluBisaGitu',
                #     'JadiWise blu bca',
                #     '#bluBuatBaik'
                #    ],
                # 'jadijago':[
                #     'Bank Jago',
                #     '@JadiJago',
                #     'BersamaKitaJago',
                #     'Gopay Jago',
                #     'BersamaKitaJagoBikinMeme',
                #     '#BersamaKitaJago',
                #     '#BibitMakinJago',
                #     '#KumpulJagoan'
                #     ],
                # 'JeniusConnect':[
                #     'Jenius Connect',
                #     '@JeniusConnect',
                #     'JeniusConnect',
                #     '@jeniushelp',
                #     'Jenius Help',
                #     'MelangkahMudah Jenius',
                #     'JeniusFuturEase',
                #     'PUNDIJenius',
                #     '#langkahkecilhariini'
                #     ],
                # 'AlloBankID':[
                #     'Allo Bank',
                #     '@AlloBankID',
                #     'AlloBank',
                #     '#RoadtoAlloBankFestival2023',
                #     '#BukaAlloBankBukaMasaDepan',
                #     '#ExperienceASimpleLife Allo Bank',
                #     '#UntungAdaAlloBank'
                #     ],
                # 'bankneocommerce':[
                #     'Bank Neo Commerce',
                #     '@bankneocommerce',
                #     'bankneocommerce',
                #     'Bank Neo',
                #     'neobank',
                #     'Neo Bank',
                #     'BuatSemua Bank Neo',
                #     'NeoWOW',
                #     '#neobank',
                #     '#BuatSemua',
                #     '#bankneocommerce',
                #     '#CuanMeowngguan'
                #     ]
                }
    # tanggal 19-25
    scraper.login()
    scroll_time = 150
    start_date='2023-08-21'
    end_date='2023-08-27'
    mode=['latest','top']
    for bank in keywords:
        scraper.search_by_account(scroll_time=scroll_time,account=bank,start_date=start_date,end_date=end_date)
        # scraper.search_by_keyword(keywords=keywords[bank],mode=mode,scroll=scroll_time,start_date=start_date,end_date=end_date,account=bank)
         # scraper.search_by_keyword(keywords=keywords,mode='top',scroll=300,start_date='2023-06-26',end_date='2023-07-02')
    scraper.save_to_excel('Twitter Bank Mega 21 agustus account.xlsx')

    # Record the end time
    end_time = time.time()
 
    # Calculate the runtime
    runtime = end_time - start_time

    # Print the runtime
    print("Runtime:", runtime, "seconds")


