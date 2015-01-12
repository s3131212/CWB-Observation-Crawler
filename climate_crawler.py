# encoding: utf-8
# create year data 2月用30天去算
def cdateList(year):
    # days31 (1,3,5,7,8,10,12) days30(2,4,6,9,11)
    month31=[1,3,5,7,8,10,12]
    nday31=range(1,32)
    nday30=range(1,31)
    day10=['01','02','03','04','05','06','07','08','09']
    month12=day10+['10','11','12']
    nday31 = map(str,nday31[9:])
    nday30 = map(str,nday30[9:])
    day31 = day10 + nday31
    day30 = day10 + nday30
    yearData=[]
    s=""
    for month,strmonth in zip(range(1,13),month12):
        if month in month31:
            for day in day31:
                s = year+'-'+strmonth+'-'+day
                yearData.append(s)
        else :
            for day in day30:
                s = year+'-'+strmonth+'-'+day
                yearData.append(s)
    return yearData
    
# 爬取主函式
def crawler(url,station,year,date):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    # find no data page
    error = soup.find(class_="imp").string.encode('utf-8')
    if error == '本段時間區間內無觀測資料。':
        with open ("./nodata.txt",'a') as f:
            f.write(url+'\n') 

    form =[]

    # title
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

# 臺南 (467410) 永康 (467420) 嘉義 (467480) 臺中 (467490) 阿里山 (467530) 新竹 (467571) 恆春 (467590)
# 成功 (467610) 蘭嶼 (467620) 日月潭 (467650) 臺東 (467660) 梧棲 (467770) 七股 (467780) 墾丁 (467790)
# 馬祖 (467990) 新屋 (467050) 板橋 (466880) 淡水 (466900) 鞍部 (466910) 臺北 (466920) 竹子湖 (466930)
# 基隆 (466940) 彭佳嶼 (466950) 花蓮 (466990) 蘇澳 (467060) 宜蘭 (467080) 金門 (467110) 東吉島 (467300)
# 澎湖 (467350) 高雄 (467440) 大武 (467540) 玉山 (467550) 
# 新竹 (467571) 真正的 url station 467570 官網標示錯誤
twStationList = ['467410','467420','467480','467490','467530','467570','467590','467610'
,'467620','467650','467660','467770','467780','467790','467990','467050','466880','466900'
,'466910','466920','466930','466940','466950','466990','467060','467080','467110','467300'
,'467350','467440','467540','467550']

# station
for station in twStationList:
    # create station folder
    dirPath = './data/'+station
    if os.path.exists(dirPath) == 0:
        os.makedirs(dirPath)
    # year
    yearList=['2013','2014']
    for year in yearList:
        dateList = cdateList(year)
        # create year folder
        dirPath = './data/'+station+'/'+year
        if os.path.exists(dirPath) == 0:
            os.makedirs(dirPath)
        # date
        for date in dateList:
            # http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=467410&datepicker=2014-11-26
            url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station="+station+"&datepicker="+date
            try:
                print(station+':'+date)
                crawler(url,station,year,date)
            except:
                print(station+':'+date+'error')
                with open ("./error.txt",'a') as f:
                    f.write(url+','+station+','+year+','+date+'\n') 

errordirPath = './error.txt'
if os.path.exists(errordirPath) == 1 :
    errorCrawler()
