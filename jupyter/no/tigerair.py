import time
import threading
class myThread (threading.Thread):
    def __init__(self, threadID,year,mon,day):
		
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.year = year
        self.mon = mon
        self.day = day
    def run (self):
        crawlerchina(self.year,self.mon,self.day)
    

def crawlerchina(year,mon,day):
    import requests
    import time
    import random
    y = year
    m = mon
    d = day
    b_y = year
    b_m = mon
    b_d = day+5
    rs = requests.session()
    while True:
        url = "https://tiger-wkgk.matchbyte.net/wkapi/v1.0/flightsearch?adults=1&children=0&infants=0&originStation=TPE&originStation=KIX&destinationStation=KIX&destinationStation=TPE&departureDate="+str(y)+"-"+str(m)+"-"+str(d)+"&departureDate="+str(b_y)+"-"+str(b_m)+"-"+str(b_d)+"&includeoverbooking=false&daysBeforeAndAfter=4&locale=en-US"
        res = rs.get(url)
        time.sleep(random.randrange(5,10))
        while True:
            if res.status_code != 200:
                res = rs.get(url)
            else:
                break
        print(res.status_code)
        # print("[INFO] crawling ")
        if len(str(m)) == 1 and len(str(d)) == 1:
            with open('D:/test/tigerair/tigerair'+str(y)+"0"+str(m)+"0"+str(d)+'.json','w') as f:
                f.write(res.text)
            print(str(y)+"0"+str(m)+"0"+str(d))
        elif len(str(m)) == 1:
            with open('D:/test/tigerair/tigerair'+str(y)+"0"+str(m)+str(d)+'.json','w') as f:
                f.write(res.text)
            print(str(y)+"0"+str(m)+str(d))
        elif len(str(d)) == 1:
            with open('D:/test/tigerair/tigerair'+str(y)+str(m)+"0"+str(d)+'.json','w') as f:
                f.write(res.text)
            print(str(y)+str(m)+"0"+str(d))
        else:
            with open('D:/test/tigerair/tigerair'+str(y)+str(m)+str(d)+'.json','w') as f:
                f.write(res.text)
            print(str(y)+str(m)+str(d))
        if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
            if d == 31:
                d = 0
                m += 1
        if m == 4 or m == 6 or m == 9 or m == 11:
            if d == 30:
                d = 0
                m += 1
        if m == 2 and d == 28:
            d = 0
            m += 1
        d += 1

        if b_m == 1 or b_m == 3 or b_m == 5 or b_m == 7 or b_m == 8 or b_m == 10 or b_m == 12:
            if b_d == 31:
                b_d = 0
                b_m += 1
        if b_m == 4 or b_m == 6 or b_m == 9 or b_m == 11:
            if b_d == 30:
                b_d = 0
                b_m += 1
        if b_m == 2 and b_d == 28:
            b_d = 0
            b_m += 1
        b_d += 1

        if m == 10 or m == 13:
            if d == 1:
                break
        if m == 1 or m == 11:
            if d == 15:
                break
        time.sleep(5)
if __name__ == '__main__':
    start_time = time.time()
    thread1 = myThread(1, 2017, 8, 15)
    thread2 = myThread(2, 2017, 10, 1)
    thread3 = myThread(3, 2017, 11, 15)
    thread4 = myThread(4, 2018, 1, 1)
    # y = 2017
    # m = 8
    # d = 1
    try:
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        end_time = time.time()
        print("spend " + str((end_time-start_time)/60) + " min")
    except:
        pass


	















