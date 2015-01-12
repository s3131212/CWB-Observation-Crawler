def date2():
    month31=[1,3,5,7,8,10,12]
    month30=[4,6,9,11]
    year2=['2012']
    nday31=range(1,32)
    nday30=range(1,31)
    nday28=range(1,29)
    day10=['01','02','03','04','05','06','07','08','09']
#     month7=['06','07','08','09','10','11','12']
    month7=['11','12']
    nday31 = map(str,nday31[9:])
    nday30 = map(str,nday30[9:])
    nday28 = map(str,nday28[9:])
    day31 = day10 + nday31
    day30 = day10 + nday30
    day28 = day10 + nday28
    output=[]
    s=""
    for year in year2:
        for month,strmonth in zip(range(11,13),month7):
            if month in month31:
                for day in day31:
                    s = year+'-'+strmonth+'-'+day
                    output.append(s)
            elif month in month30:
                for day in day30:
                    s = year+'-'+strmonth+'-'+day
                    output.append(s)
            else:
                for day in day28:
                    s = year+'-02-'+day
                    output.append(s)
    return output

def crawler(name):
    print(name)
    # http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467410&datepicker=2014-11-26
    url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467410&datepicker="+name
    print(url)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    form =[]
    # title
    second_tr = soup.find(class_="second_tr")
    titles = soup.find_all("th")
    titles = titles[9:]
    strtitle=[]
    for title in titles:
        title = title.contents
        title=title[0]+title[2]+title[4]
        strtitle.append(title)

    # parameter
    soup = soup.tbody
    tmps = soup.find_all("tr")
    tmps = tmps[2:]
    for tmp in tmps:
        tmp = tmp.find_all("td")
        parameter =[]
        for strtmp in tmp:
            strtmp = strtmp.string
            parameter .append(strtmp)
        form.append(parameter)

    form = pd.DataFrame(form, columns=strtitle)
    sleep(0.2)
#     form.to_csv("/Users/wy/Desktop/climate/"+name+".txt", encoding ="utf-8")
    # sleep(0.5)

# -*- coding: utf-8 -*- 
import requests
import datetime
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

st = datetime.datetime.now() 


import time, threading, datetime  
from Queue import Queue
  
bbb = date2()

class Job:    
    def __init__(self, name):
        self.name = name    
    def do(self):
        try:
            crawler(self.name)
        except:
            sleep(1)
            crawler(self.name)

que = Queue()  
for tmp in bbb:
    que.put(Job(tmp))

def doJob(*args):  
     queue = args[0]  
     while queue.qsize() > 0:  
          job = queue.get()
          print(job) 
          job.do()  
  
# Open three threads  
thd1 = threading.Thread(target=doJob, name='Thd1', args=(que,))  
thd2 = threading.Thread(target=doJob, name='Thd2', args=(que,))  
thd3 = threading.Thread(target=doJob, name='Thd3', args=(que,))  
  
# Start activity to digest queue.  
thd1.start()
thd2.start() 
thd3.start()  
  
# Wait for all threads to terminate.  
while thd1.is_alive() or thd2.is_alive() or thd3.is_alive():  
     time.sleep(1)    
 
for date in bbb:
    try:
        crawler(date)
    except:
        pass
td = datetime.datetime.now()  
print(td-st)
