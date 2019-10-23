import calendar

import ec as ec
import requests
import json
import sys
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import jenkins
from pymongo import MongoClient
from datetime import datetime
import smtplib
from configparser import ConfigParser
import ast
import logging
from threading import *
import threading



class Jenkins_Automation:

    repo_list = []
    exist_job = []

    def __init__(self):
        self.logger = self.logging_info()
        self.logger.info('Getting config detail')
        configParser = ConfigParser()
        configParser.read('data.config')
        self.jenkins_dict = ast.literal_eval(configParser.get('jenkins_detail', 'jenkins_dict'))
        print("jenkins_dict ",type(self.jenkins_dict))
        self.url = self.jenkins_dict['url']
        self.logger.info("Opening chrome browser")
        self.browser = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver')
        self.jenkins_username = self.jenkins_dict['username']
        self.jenkins_password = self.jenkins_dict['password']
        self.jenkins_server = jenkins.Jenkins(self.url, username=self.jenkins_username, password=self.jenkins_password)

    def logging_info(self):
        logger = logging.getLogger('demologger')
        logger.setLevel(logging.INFO)
        #create console and file handler
        consoleHandler = logging.StreamHandler()
        fileHandler = logging.FileHandler('abc.log', mode='w')
        #set level
        consoleHandler.setLevel(logging.INFO)
        fileHandler.setLevel(logging.INFO)
        #set format
        formatter = logging.Formatter('%(asctime)s-%(levelname)s:%(msg)s')
        consoleHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)
        #add file and console handler
        logger.addHandler(consoleHandler)
        logger.addHandler(fileHandler)
        return logger

    def get_all_repos(self):
        self.login_jenkins()
        self.logger.info("Gettting all repos from github")
        #self.repo_list = []
        git_api = "https://api.github.com/users/Terralogic-Sarosh/repos"
        try:
            response = requests.get(git_api)
        except requests.exceptions.RequestException as error:
            self.logger.critical(error)
            sys.exit(1)
        if response.ok:
            json_data = json.loads(response.content)
            for dict in json_data:
                Jenkins_Automation.repo_list.append(dict['name'])
            print(self.repo_list)
            return self.repo_list
        else:
            print("No response")
            sys.exit(1)

    def login_jenkins(self):
        self.browser.get(self.url)
        self.browser.find_element_by_name('j_username').send_keys('admin')
        self.browser.find_element_by_name('j_password').send_keys('6f0538b3fb304d918a5c7d2675221c66')
        self.browser.find_element_by_name('Submit').click()

    def get_existing_job(self):
        #exist_job = []
        self.logger.info("Getting exist job in jenkins")
        exist_job_data = self.jenkins_server.get_all_jobs()
        for data in exist_job_data:
            Jenkins_Automation.exist_job.append(data['name'])
        self.logger.info("Existing job in jenkins : {}".format(self.exist_job))

    def create_new_job(self):
        self.get_all_repos()
        self.get_existing_job()
        git_url = "https://github.com/Terralogic-Sarosh/"
        for repo in self.repo_list:
            if repo in self.exist_job:
                print('{} job already exist in Jenkins'.format(repo))
                continue
            #selecting new job
            self.browser.find_element_by_xpath('//*[@id="tasks"]/div[1]/a[2]').click()
            time.sleep(2)
            # creating jenkins job for each repo
            self.browser.find_element_by_name('name').send_keys(repo)
            self.browser.find_element_by_xpath('//*[@id="j-add-item-type-standalone-projects"]/ul/li[1]/label/span').click()
            self.browser.find_element_by_id('ok-button').click()
            time.sleep(2)
            #filling git repo url
            repo_url = git_url+repo
            self.browser.find_element_by_xpath('// *[ @ id = "main-panel"] / div / div / div / div[2] / div[3] / div / div[2]').click()
            time.sleep(2)
            self.browser.find_element_by_id('radio-block-1').click()
            self.browser.find_element_by_name('_.url').send_keys(repo_url)
            time.sleep(3)
            #Adding credentials
            self.browser.find_element_by_name('_.credentialsId').click()
            #clicking first credential
            arrow_down = ActionChains(self.browser).send_keys(Keys.ARROW_DOWN)
            arrow_down.click().perform()
            time.sleep(3)
            #apply and save
            self.browser.find_element_by_id('yui-gen28-button').click()
            time.sleep(1)
            self.browser.find_element_by_id('yui-gen42-button').click()
            time.sleep(2)
            #back to the dashboard
            self.browser.find_element_by_xpath('//*[@id="tasks"]/div[1]/a[2]').click()
            time.sleep(2)

    def trigger_jenkin_job(self, job):

        self.logger.info("################# {} #################".format(job))
        build_info = self.get_latest_build_info(job)
        print("build info for {} job : ".format(job), build_info)
        #for newly job who did not build once till now
        if build_info == None:
            pre_timestamp = int(datetime.now().timestamp() * 1000)
            print("pre_timestamp {} for first build of job {} ".format(pre_timestamp, job))
        else:
            pre_timestamp = build_info['timestamp']
        #current_timestampt_1 = datetime.now().timestamp()
        #print("########### current_timestampt_1 #####################", current_timestampt_1)
        #current_timestampt_2 = time.time()
        #print("########### current_timestampt_2 #####################", current_timestampt_2)
        #current_timestampt_3 = calendar.timegm(time.gmtime())
        #print("########### current_timestampt_3 #####################", current_timestampt_3)

        print("Triggering job for repo {}".format(job))
        self.jenkins_server.build_job(job)
        self.get_build_result(job, pre_timestamp)

    def get_build_result(self, job, pre_timestamp):
        while(True):
            build_info = self.get_latest_build_info(job)
            print("build info in while for job {} : ".format(job), build_info)
            #Condition for fist build of the job
            if build_info == None:
                self.logger.info("Getting build result for first build of job : {}".format(job))
                time.sleep(2)
                continue
            post_timestamp = build_info['timestamp']
            print("pre_timestamp %s post_timestamp %s"%(pre_timestamp, post_timestamp))
            if pre_timestamp == post_timestamp or build_info['building'] == True:
                print('Running....')
                time.sleep(2)
            else:
                break
        print('Stop....')
        now = datetime.now()
        current_time = now.strftime("%d:%m:%Y %H:%M:%S")
        self.build_result[job] = {'time': current_time, 'build_no':build_info['number'], 'result':build_info['result']}
        return self.build_result

    def get_latest_build_info(self, job):
        job_info = self.jenkins_server.get_job_info(job)
        builds = job_info['builds']
        if len(builds) == 0:
            return None
        else:
            build_info = self.jenkins_server.get_build_info(job, builds[0]['number'])
            return build_info

    def trigger_job_and_get_build_result(self):
        self.create_new_job()
        self.build_result = {}
        thread_list = ["t"+str(i) for i in range(len(self.repo_list))]
        print("thread_list", thread_list)
        i = 0
        for job in self.repo_list:
            thread_list[i] = threading.Thread(target=self.trigger_jenkin_job,args=(job,))
            thread_list[i].start()
            self.logger.info("Thread {} for job {} started".format(thread_list[i], job))
            i += 1
        while(True):
            if(len(self.build_result) == len(self.repo_list)):
                break
            else:
                self.logger.info("Calculating the build_result of all the Job's")
                time.sleep(2)
        self.logger.info("Final Build Results")
        self.logger.info(self.build_result)
        self.update_data()
        self.send_mail()

    def update_data(self):
        #self.build_result = {'FifthProject': {'time': '11:10:2019 17:44:28', 'build_no': 65, 'result': 'SUCCESS'}, 'FourthProject': {'time': '11:10:2019 17:44:28', 'build_no': 61, 'result': 'SUCCESS'}, 'SecondProject': {'time': '11:10:2019 17:44:29', 'build_no': 61, 'result': 'SUCCESS'}, 'seven_project': {'time': '11:10:2019 17:44:31', 'build_no': 61, 'result': 'SUCCESS'}, 'Six-Project': {'time': '11:10:2019 17:44:32', 'build_no': 61, 'result': 'SUCCESS'}, 'Hello_World': {'time': '11:10:2019 17:44:34', 'build_no': 82, 'result': 'FAILURE'}, 'ThirdProject': {'time': '11:10:2019 17:44:34', 'build_no': 61, 'result': 'SUCCESS'}}
        self.logger.info(" !!! Updating data in the database !!! ")
        client = MongoClient('127.0.0.1', 27017)
        db = client.test
        print("update data ", db)
        db.demo_collection.insert_one(self.build_result)
        print("id", id)
        inserted_data = list(db.demo_collection.find())
        print("inserted_data type", type(inserted_data))
        last_inserted_data = inserted_data[len(inserted_data)-1:len(inserted_data)]
        print("last_inserted_data", last_inserted_data)
        print("build_result", self.build_result)
        print("inserted_data", inserted_data)
        if self.build_result in last_inserted_data:
            self.logger.info(" !!! Hurra !!! @@@ Data Updated Succcessfully @@@")

    def send_mail(self):
        self.logger.info(" !!! Sending emails !!! ")
        sender = 'sarosh32ahmad@gmail.com'
        receiver = ['bayssarosh@gmail.com']
        message = """From Person %s
        To: To Person %s
        MIME-Version: 1.0
        Content-type: text/html
        Subject: Jenkins Build results
        
        <b>This is html message.</b>
        <h1>%s</h1>."""%(sender, receiver, self.build_result)

        message = 'Subject: {}\n\n{}'.format('Jenkins Build results', message)
        print(message)
        try:
            smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpobj.starttls()
            smtpobj.login(sender, '121aa121sss')
            smtpobj.sendmail(sender, receiver, message)
            smtpobj.quit()
        except Exception as error:
            print(error)
            sys.exit(1)













obj = Jenkins_Automation()
#repo_list =  obj.get_all_repos()
#obj.login_jenkins()
#exist_job = obj.get_existing_job()
#obj.create_new_job()
#build_results = obj.trigger_jenkin_job(repo_list)
obj.trigger_job_and_get_build_result()
#build_results = {'FifthProject': {'time': '04:10:2019 12:28:40', 'build_no': 22, 'result': 'SUCCESS'}, 'FourthProject': {'time': '04:10:2019 12:28:40', 'build_no': 23, 'result': 'SUCCESS'}, 'Hello_World': {'time': '04:10:2019 12:28:41', 'build_no': 44, 'result': 'FAILURE'}, 'SecondProject': {'time': '04:10:2019 12:28:41', 'build_no': 23, 'result': 'SUCCESS'}, 'seven_project': {'time': '04:10:2019 12:28:41', 'build_no': 23, 'result': 'SUCCESS'}, 'Six-Project': {'time': '04:10:2019 12:28:41', 'build_no': 23, 'result': 'SUCCESS'}, 'ThirdProject': {'time': '04:10:2019 12:28:48', 'build_no': 23, 'result': None}}
#build_results = obj.get_build_result(repo_list)
#obj.update_data()
#obj.send_mail(self.build_results)


