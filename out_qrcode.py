import qrcode
import json
from PIL import Image
import numpy as np
import os
import qrtools


address_array =[]

def make_qrcode():
    k = 0
    l = 0
    Address = {}

    with open('sponsor50.txt','r') as f:
        temp = json.loads(f.read())
    for x in temp['Keys']:
        Address[k] = x["Address"]
        print(Address[k])
#        print(Address[k][:10])
        k += 1

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    for i in range(2000):
#        if(i%35==0):
#            l += 1
#            os.mkdir('qrcode%s'%l)
        qr.clear()
        qr.add_data(Address[i])
        qr.make(fit=True)

#        img = qr.make_image(fill_color="black", back_color="white")
#        img = img.resize((240,240))
#        img.save("qrcode_sponsor/Private%s.png"%(i))
#        qr = qrtools.QR()
#        qr.decode("qrcode2000/%s.png"%(i))
#        if(qr.data!=Address[i]):
#            print(i,'error')
#            break


def marge_qrcode():
    t = 0
    QR = []
    for i in range(50):
        im = Image.open("qrcode/qrcode%s.png"%i)
        QR[i] = im.resize((290,290))
    Back = Image.new('RGBA', (2100, 2910),0)

    for x in range(10): #width
        for y in range(7): #height
            if(QR[i] == None):
                break
            else:
                Back.paste(QR[t],(x*292,y*292),(290,290))
    Back.save("marge.png")


if __name__ == '__main__':
    make_qrcode()
#    marge_qrcode()
