from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import os
import sys

def get_holder(token_contract):
    path = os.getcwd()
    os.environ["PATH"] += ':' + path

    i = 0
    Holder = {}
    holder_json = {}
    holder_json["list"] = []
    holder_json["number"] = []

#    holder_json.append('{"list":')

    browser = webdriver.Firefox()
    browser.set_window_size(1280,800)
    Net = "https://ropsten.etherscan.io/token/" + token_contract + "#balances"
    browser.get(Net)

    Wait = WebDriverWait(browser, 10)
    Wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='tokeholdersiframe']")))

    browser.switch_to.frame("tokeholdersiframe")

    while(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/span/a[3]"))):
#    while(browser.find_element_by_xpath("/html/body/div[2]/span/span/b[1]").text < browser.find_element_by_xpath("/html/body/div[2]/span/span/b[2]").text):
        data = BeautifulSoup(browser.page_source)
        for x in data.find_all('span'):
            temp = str(x)
            if(temp[:22] == '<span><a href="/token/'):
                Holder[i] = temp[67:109]
#                print(i+1,"Holder:", Holder[i])
                node = {
                "Holder" : Holder[i]
                }
                holder_json["list"].append(node)
                i += 1
        if(int(browser.find_element_by_xpath("/html/body/div[2]/span/span/b[1]").text) < int(browser.find_element_by_xpath("/html/body/div[2]/span/span/b[2]").text)):
            browser.find_element_by_xpath("/html/body/div[2]/span/a[3]").click()
            Wait = WebDriverWait(browser, 10)
            Wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/table")))
        else:
            break
    browser.switch_to.default_content()
    holder_number = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[1]/table/tbody/tr[2]/td[2]').text
    holder_json["number"].append({"Number" : holder_number[:-10]})

    with open('holder_list.txt', 'w') as f:
        f.write(json.dumps(holder_json))

    browser.close()

def find_half():
    n = 0
    total = 0
    Holder = {}
    holder_json = {}
    holder_json["half_list"] = []

    with open('holder_list.txt', 'r') as fr:
        data = json.load(fr)
        for x in data["list"]:
#            print(x["Holder"])
            Holder[n] = x["Holder"]
            n += 1
        for y in data["number"]:
            total = int(y["Number"])
            print(total)
#    for i in range(int(total/2)):
    for i in range(50):
#        if(i<1000):
#            node = {
#            "Holder" : Holder[i]
#            }
#            holder_json["half_list"].append(node)
            print('{"',Holder[i],'":"10"},')

    with open('half_holder_list.txt', 'w') as f:
        f.write(json.dumps(holder_json))

def get_transaction(token_contract):
    j = 0
    k = 0
    From = {}
    To = {}
    trans_json = {}
    trans_json["list"] = []

    path = os.getcwd()
    os.environ["PATH"] += ':' + path

    browser = webdriver.Firefox()
    browser.set_window_size(1280,800)
    Net = "https://ropsten.etherscan.io/token/" + token_contract
    browser.get(Net)

    Wait = WebDriverWait(browser, 10)
    Wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tokentxnsiframe"]')))

    browser.switch_to.frame("tokentxnsiframe")

    while(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr[2]/td[1]/span/a"))):
        data = BeautifulSoup(browser.page_source)
        x = data.find_all('span', 'address-tag')
        for j in range(0, len(x), 3):
            j += 1
            temp = str(x[j])
            trans_json["list"].append({"F_A": "", "T_A": ""})
            new_trans = trans_json["list"][-1]
            From[k] = temp[141:183]
#            print(k+1,'From:',From[k])
            new_trans["F_A"] = From[k]
            j += 1
            temp = str(x[j])
            To[k] = temp[141:183]
#            print(k+1,'To:',To[k])
            new_trans["T_A"] = To[k]
            k += 1
        if(int(browser.find_element_by_xpath("/html/body/div[2]/div[1]/span/span/b[1]").text) < int(browser.find_element_by_xpath("/html/body/div[2]/div[1]/span/span/b[2]").text)):
            browser.find_element_by_xpath("/html/body/div[2]/div[1]/span/a[3]").click()
            Wait = WebDriverWait(browser, 10)
            Wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr[2]/td[1]/span/a")))
            time.sleep(1)
        else:
            break
    browser.switch_to.default_content()
    with open('trans_list.txt', 'w') as f:
        f.write(json.dumps(trans_json))

    browser.close()

def transfer_count():
    i = 0
    j = 0
    from_address = []
    to_address = []
    transfer_out = []
    transfer_in = []


    with open('trans_list.txt', 'r') as fr:
        data = json.load(fr)
        for x in data['list']:
            from_address.append(x['F_A'])

        for x in data['list']:
            to_address.append(x['T_A'])

#how many transfer from address
    for x in range(0,len(from_address)):
        temp = from_address[x]
        if temp not in transfer_out:
            transfer_out.append(temp)

#how many transfer to address
    for x in range(0,len(to_address)):
        temp = to_address[x]
        if temp not in transfer_in:
            transfer_in.append(temp)

    for x in range(0,len(transfer_out)):
        sort_out = from_address.count(transfer_out[x])
        print(x+1,transfer_out[x],':',sort_out)

    i = 0
    for x in range(0,len(transfer_out)):
        sort_out = from_address.count(transfer_out[x])
#        print(x+1,transfer_out[x],':',sort_out)
#        if(sort_out >= 4):
#            i += 1
#            print(transfer_in[x][:6],sort_out,'times','{"',transfer_out[x],'":"3"},')
#    print('in:',i)

    for x in range(0,len(transfer_in)):
        sort_in = to_address.count(transfer_in[x])
#        print(x+1,transfer_in[x],':',sort_in)

    o = 0
    for x in range(0,len(transfer_in)):
        sort_in = to_address.count(transfer_in[x])
#        print(x+1,transfer_in[x],':',sort_in)
        if(sort_in >= 4):
            o += 1
            print(transfer_in[x][:6],sort_in,'times','{"',transfer_in[x],'":"2"},')
    print('out:',o)



#path = os.getcwd()
#os.environ["PATH"] += ':' + path

if __name__ == '__main__':

#    while(1):
#        Token = input("Token Contract:")
#        if((len(Token)!=42) and (Token[0:1]!="0x")):
#            print("Please input token contract!")
#        else:
#            Right_Token = Token
#            print("Your Token Contract is : ",Right_Token)
#            break

    Right_Token = '0x503b0c139665e7e9f863ba1bcf0e635a2e87aa5b'

#    get_holder(Right_Token)
#    find_half()
#    get_transaction(Right_Token)
    transfer_count()
