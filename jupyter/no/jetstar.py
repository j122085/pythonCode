import splinter
import re
import random
import time
import pymongo
from pymongo import MongoClient

browser = splinter.Browser(driver_name='chrome')
time.sleep(random.randrange(1,2))
go_y = 2017
go_m = 8
go_d = 15
back_y = 2017
back_m = 8
back_d = 19
while True:

    browser.visit("http://www.jetstar.com/tw/zh/home?origin=TPE&destination=KIX&flight-type=2&adult=1&currency=TWD&selected-departure-date=" + str(go_d) + "-" + str(go_m) + "-"+ str(go_y) + "&selected-return-date=" + str(back_d) + "-" + str(back_m) + "-" + str(back_y))

    time.sleep(random.randrange(5,10))
    browser.find_by_css('.js-flight-search-submit').click()
    time.sleep(10)
    while True:
        print(browser.url)
        if browser.url == "http://www.jetstar.com/tw/zh/home":
            browser.visit("http://www.jetstar.com/tw/zh/home?origin=TPE&destination=KIX&flight-type=2&adult=1&currency=TWD&selected-departure-date=" + str(go_d) + "-" + str(go_m) + "-"+ str(go_y) + "&selected-return-date=" + str(back_d) + "-" + str(back_m) + "-" + str(back_y))
            time.sleep(random.randrange(10,20))
            browser.find_by_css('.js-flight-search-submit').click()
            time.sleep(random.randrange(10,20))
        else:
            break
    
    # browser.find_by_css('.js-flight-search-submit').click()

    time.sleep(random.randrange(10,20))

    hid = browser.find_by_css('.info-show')

    time.sleep(random.randrange(1,2))

    for show in hid:
        try:
            show.click()
        except:
            pass

    go = browser.find_by_id("economy-TPE")

    go_str = go.text.replace("\n","").replace(":","-").replace(",","")

    n = 0

    while True:
        try:
            dir = {}
            dir['Departtime'] = str(go_y) + '-' + str(go_m) + '-' + str(go_d) + '-' + re.findall("(\d+\-\d+)TPE - 出發",go_str)[n]
            dir['arrivaltime'] = str(go_y) + '-' + str(go_m) + '-' + str(go_d) + '-' + re.findall("(\d+\-\d+)KIX - 到達",go_str)[n]
            dir['No'] = re.findall("選擇航班1：(\w+\d+)",go_str)[n]
            dir['Price'] = re.findall('旅程隱藏TWD(\d+)',go_str)[n]
            dir['Depart'] = 'TPE'
            dir['Arrival'] = 'KIX'
            dir['Chiname'] = '捷星'
            dir['Engname'] = 'JETSTAR'

            client = MongoClient()
            db=client["bb102"]
            collection=db["airline"]
            collection.insert(dir)
            time.sleep(random.randrange(3,5))
            n += 1
            print(go_y+" "+go_m+" "+go_d)
            if n > int(len(re.findall("(\d+\-\d+)TPE - 出發",go_str))) - 1:
                break
        except:
            break

    back = browser.find_by_id("economy-KIX")

    back_str = back.text.replace("\n","").replace(":","-").replace(",","")

    n = 0
    while True:
        try:
            dir = {}
            dir['Departtime'] = str(back_y) + '-' + str(back_m) + '-' + str(back_d) + '-' + re.findall("(\d+\-\d+)KIX - 出發",back_str)[n]
            dir['arrivaltime'] = str(back_y) + '-' + str(back_m) + '-' + str(back_d) + '-' + re.findall("(\d+\-\d+)TPE - 到達",back_str)[n]
            dir['No'] = re.findall("選擇航班1：(\w+\d+)",back_str)[n]
            dir['Price'] = re.findall('旅程隱藏TWD(\d+)',back_str)[n]
            dir['Depart'] = 'KIX'
            dir['Arrival'] = 'TPE'
            dir['Chiname'] = '捷星'
            dir['Engname'] = 'JETSTAR'

            client = MongoClient()
            db=client["bb102"]
            collection=db["airline"]
            collection.insert(dir)

            time.sleep(random.randrange(3,5))
            print(back_y+" "+back_m + " " +back_d)
            n += 1
            if n > int(len(re.findall("(\d+\-\d+)KIX - 出發",back_str))) - 1:
                break
        except:
            break
    if go_m == 8 or go_m == 10:
        if go_d == 31:
            go_m += 1
            go_d = 0

    if go_m == 9 or go_m == 11:
        if go_d == 30:
            go_m += 1
            go_d = 0

    if go_m == 12:
        if go_d == 31:
            go_y = 2018
            go_m = 1
            go_d = 0

    go_d += 1

    if back_m == 8 or back_m == 10:
        if back_d == 31:
            back_m += 1
            back_d = 0

    if back_m == 9 or back_m == 11:
        if back_d == 30:
            back_m += 1
            back_d = 0

    if back_m == 12:
        if back_d == 31:
            back_y = 2018
            back_m = 1
            back_d = 0

    back_d += 1

    if go_y == 2018 and go_m == 1 and go_d == 28:
        break





