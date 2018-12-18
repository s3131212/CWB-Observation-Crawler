# Config
# 測站編號，以下是台北市的所有測站
twStationList = ["466910", "466920", "466930", "C0A980", "C0A990", "C0A9A0", "C0A9B0", "C0A9C0", "C0A9E0", "C0A9F0", "C0AC40", "C0AC70", "C0AC80", "C0AH40", "C0AH70", "C1A730", "C1AC50"]
# 年份
yearList=['2017', '2018']
# 月份
monthSearch = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# encoding: utf-8
# create year data 2月用30天去算
def cdateList(year):
    # days31 (1,3,5,7,8,10,12) days30(2,4,6,9,11)
    month31=[1,3,5,7,8,10,12]
    yearData=[]
    s=""
    for month in monthSearch:
        if month in month31:
            for day in range(1, 32):
                s = year + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
                yearData.append(s)
        else :
            for day in range(1, 31):
                s = year + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
                yearData.append(s)
    return yearData
    
# 爬取主函式
def crawler(url,station,year,date):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features="html.parser")

    # find no data page
    error = soup.find("label", class_="imp").string

    if error == '本段時間區間內無觀測資料。':
        print(station+':'+date+' 無觀測資料')
        with open ("./nodata.txt",'a') as f:
            f.write(url+'\n')
        return

    form =[]

    # title
    titles = soup.find_all("th")
    titles = titles[11:28]
    strtitle=[]
    for title in titles:
        title = title.contents
        title=title[0] #+title[2]+title[4]
        strtitle.append(title)

    # parameter
    soup = soup.tbody
    tmps = soup.find_all("tr")
    tmps = tmps[2:]
    for tmp in tmps:
        tmp = tmp.find_all("td")
        parameter =[]
        for strtmp in tmp:
            strtmp = ''.join(filter(lambda x: (x.isdigit() or x == '.'  or x == 'T'), strtmp.string))
            parameter.append(strtmp)
        form.append(parameter)

    form = pd.DataFrame(form, columns=strtitle)
    form.to_csv("./data/"+station+'/'+year+'/'+date+".csv", encoding ="utf-8")
    # sleep(0.5)

 # 有分nodata.txt 和 error.txt，nodata.txt是指網站沒資料
 # error.txt 可能是連線失敗或是沒抓到，因此兩組相對再去抓沒抓到的
def errorCrawler():
    nodatadirPath = './nodata.txt'
    if os.path.exists(nodatadirPath) == 1 :   
        with open ("./nodata.txt",'r') as f:
            nodataUrls = f.readlines()
        with open ("./error.txt",'r') as f:
            urls = f.readlines()
            for url in urls:
                url = url.strip()
                url = url.split(',')
                compareUrl = url[0]+'\n'
                # 對照nodata.txt，本來就沒有資料就不抓
                if compareUrl in nodataUrls:
                    pass
                else:
                    try:
                        sleep(1)
                        crawler(url[0],url[1],url[2],url[3])
                        print('again:'+url[1]+','+url[2]+','+url[3])
                        # 再次紀錄第二次抓哪些資料
                        with open ("./error_reCrawler.txt",'a') as f:
                            f.write(url[0]+','+url[1]+','+url[2]+','+url[3]+'\n')
                    except :
                        print('error:'+url[1]+','+url[2]+','+url[3])
    else:
        with open ("./error.txt",'r') as f:
            urls = f.readlines()
            for url in urls:
                url = url.strip()
                url = url.split(',')
                sleep(1)
                print('again:'+url[1]+','+url[2]+','+url[3])
                crawler(url[0],url[1],url[2],url[3])

# -*- coding: utf-8 -*- 
import os
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

# station
for station in twStationList:
    # create station folder
    dirPath = './data/'+station
    if os.path.exists(dirPath) == 0:
        os.makedirs(dirPath)

    for year in yearList:
        dateList = cdateList(year)
        # create year folder
        dirPath = './data/'+station+'/'+year
        if os.path.exists(dirPath) == 0:
            os.makedirs(dirPath)
        # date
        for date in dateList:
            # http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466910&stname=&datepicker=2018-12-11
            url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station="+station+"&stname=&datepicker="+date
            try:
                print(station+':'+date)
                crawler(url,station,year,date)
            except Exception as e:
                print(station + ':' + date + ' Error!' + ' Code: {c}, Message: {m}'.format(c = type(e).__name__, m = str(e)))
                with open ("./error.txt",'a') as f:
                    f.write(url+','+station+','+year+','+date+'\n') 

errordirPath = './error.txt'
if os.path.exists(errordirPath) == 1 :
    errorCrawler()
