from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import sys

path = os.getcwd()
os.environ["PATH"] += ':' + path

Contract = '0x84e0b37e8f5b4b86d5d299b0b0e33686405a3919'
Holder = '0x38ba9213c70bf6fe34f70cfc5c9b26707c6c1e85'
i = 0
j = 0
k = 0
TxHash = {}
From = {}
To = {}

try:
    browser = webdriver.Firefox()
    browser.set_window_size(1240,800)
    Net = "https://ropsten.etherscan.io/token/" + Contract + "?a=" + Holder
    browser.get(Net)

    Wait = WebDriverWait(browser, 10)
    Wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='tokentxnsiframe']")))

    browser.switch_to.frame('tokentxnsiframe')

    while(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/span/a[3]"))):
        data = BeautifulSoup(browser.page_source)
#    print(data.find_all('span', 'address-tag'))
        for x in data.find_all('span', 'address-tag'):
#        print(x)
            temp = str(x)
            if(temp[:39] == '<span class="address-tag"><a href="/tx/'):
                TxHash[i] = temp[39:105]
                print(i+1,'TxHash:',TxHash[i])
                i += 1
            if(temp[:28] == '<span class="address-tag">0x'):
                From[j] = temp[26:68]
                print(j+1,'From:',From[j])
                j += 1
            if(temp[:37] == '<span class="address-tag"><a href="0x'):
                To[k] = temp[141:183]
                print(k+1,'To:',To[k])
                k += 1

        browser.find_element_by_xpath("/html/body/div[2]/div[1]/span/a[3]").click()
        Wait = WebDriverWait(browser, 10)
        Wait.until(EC.presence_of_element_located((By.XPATH, "/html")))


    browser.switch_to.default_content()


finally:
    browser.close()
    print('final')
