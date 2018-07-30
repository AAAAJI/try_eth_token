from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import os
import sys

path = os.getcwd()
os.environ["PATH"] += ':' + path

k = 0
l = 0
Address = {}
#browser = webdriver.Firefox()
#browser.set_window_size(800,600)

try:
    with open('dump_keys.txt', 'r') as fp:
        data = json.loads(fp.read())
    for x in data['Keys']:
#        print(x["Address"])
        Address[k] = x["Address"]
        k += 1

    for x in range(100):
        browser = webdriver.Firefox()
        browser.set_window_size(800,600)
        for y in range(20):
            Net = 'https://ropsten.etherscan.io/address/' + Address[l]
            browser.get(Net)

            Wait = WebDriverWait(browser, 20, 5)
            Wait.until(EC.presence_of_element_located((By.ID, 'transactions')))

            if(browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div[1]/div/div/table/tbody/tr[2]/td[7]").text == '1 Ether'):
                print(l,'.',browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div[1]/div/div/table/tbody/tr[2]/td[6]/span").text,'sucess!')
            else:
                print(l,'.',Address[l],'Failed')
            l += 1
        browser.close()

finally:
    print('final')
