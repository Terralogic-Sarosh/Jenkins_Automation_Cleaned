from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

browser = webdriver.Chrome(executable_path="D:\chromedriver_win32\chromedriver")
browser.get("http://localhost:8080/")


j_username = browser.find_element_by_id('j_username')

j_username.send_keys('admin')

#psw=input('enter psw: ')

j_pass = browser.find_element_by_name('j_password')

j_pass.send_keys('6f0538b3fb304d918a5c7d2675221c66')

submit = browser.find_element_by_name('Submit').click()
time.sleep(2)
newjob =browser.find_element_by_xpath('//*[@id="tasks"]/div[1]/a[2]').click()

time.sleep(2)
j_name = browser.find_element_by_id('name')

j_name.send_keys('t3')
b1=browser.find_element_by_xpath('//*[@id="j-add-item-type-standalone-projects"]/ul/li[1]').click()

ok1 =browser.find_element_by_xpath('//*[@id="ok-button"]').click()
time.sleep(3)
gitsc = browser.find_element_by_xpath('//*[@id="main-panel"]/div/div/div/div[2]/div[3]/div/div[2]').click()
#gitsc = browser.find_element_by_xpath('//*[@id="main-panel"]/div/div/div/div[2]/div[3]/div/div[3]').click()
time.sleep(2)

gitradio = browser.find_element_by_xpath('//*[@id="radio-block-1"]').click()


time.sleep(2)

repositoryurl = browser.find_element_by_xpath('//*[@id="main-panel"]/div/div/div/form/table/tbody/tr[97]/td[3]/div/div[1]/table/tbody/tr[1]/td[3]/input')

time.sleep(2)
repositoryurl.send_keys('https://github.com/Terralogic-Sarosh/SecondProject')
time.sleep(2)
crd = browser.find_element_by_xpath('//*[@id="main-panel"]/div/div/div/form/table/tbody/tr[97]/td[3]/div/div[1]/table/tbody/tr[4]/td[3]/div/div/select').click()
a=ActionChains(browser).send_keys(Keys.ARROW_DOWN)
a.click().perform()
time.sleep(1)
save = browser.find_element_by_xpath('//*[@id="yui-gen39-button"]').click()

time.sleep(2)
build= browser.find_element_by_xpath('//*[@id="tasks"]/div[5]/a[2]').click()