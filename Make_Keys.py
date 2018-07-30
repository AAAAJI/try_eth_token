from ecdsa import SigningKey, SECP256k1
import sha3
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import sys

path = os.getcwd()
os.environ["PATH"] += ':' + path

def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out
x = 0
#browser = webdriver.Firefox()

try:
    json_array = []
#    for x in range(10):
    while(1):
        keccak = sha3.keccak_256()
        priv = SigningKey.generate(curve=SECP256k1)
        pub = priv.get_verifying_key().to_string()

        keccak.update(pub)
        address = keccak.hexdigest()[24:]


        json_node = {
        "Address" : checksum_encode(address),
        "Public" : pub.hex(),
        "Private" : priv.to_string().hex()
        }
#Get 1 eth
        browser = webdriver.Firefox()
        Net = 'http://faucet.ropsten.be:3001/donate/' + checksum_encode(address)
        browser.get(Net)
        list = (x ,Net)
        print(list)

#Check first time
        Wait = WebDriverWait(browser, 10)
        Wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='treeLabel stringLabel']")))
#        print(browser.find_element(By.XPATH, "//span[@class='treeLabel stringLabel']").text)

# Check OK and add
        if(browser.find_element(By.XPATH, "//span[@class='treeLabel stringLabel']").text == 'msg'):
            print('Failed')
        else:
            json_array.append(json_node)
            print('success add', checksum_encode(address))
            x += 1

        browser.close()

        time.sleep(5)

        if(x == 500):
            print("The ",x,"account already finish")
            break

    with open('dump_keys.txt', 'w') as fp:
        fp.write(json.dumps(json_array))

finally:
    browser.close()
    with open('dump_keys.txt', 'w') as fp:
        fp.write(json.dumps(json_array))
