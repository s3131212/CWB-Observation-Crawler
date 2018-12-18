# 中央氣象局觀測資料查詢系統（CODiS）爬蟲

## 簡介
此爬蟲會把[中央氣象局觀測資料查詢系統（CWB Observation Date Inquire System, CODiS）](http://e-service.cwb.gov.tw/HistoryDataQuery/)的資料爬下來，並以 csv 儲存，支援失敗再次下載。

## 用法
打開 `climate_crawler.py` 並修改檔案開頭的 config
```python
# 測站編號，以下是台北市的所有測站
twStationList = ["466910", "466920", "466930", "C0A980", "C0A990", "C0A9A0", "C0A9B0", "C0A9C0", "C0A9E0", "C0A9F0", "C0AC40", "C0AC70", "C0AC80", "C0AH40", "C0AH70", "C1A730", "C1AC50"]
# 年份
yearList=['2017', '2018']
# 月份
monthSearch = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```
（測站編號請至 [CODiS](http://e-service.cwb.gov.tw/HistoryDataQuery/) 查詢）

修改後執行 `python3 climate_crawler.py`，資料會被下載於 /data 中

還沒修改 [multi_crawler.py](https://github.com/s3131212/CWB-Observation-Crawler/blob/master/multi_crawler.py)（多執行緒版本），PR Welcome!

## 版權聲明
此程式修改自 [wy36101299/crawler-central-weather](https://github.com/wy36101299/crawler-central-weather)，此程式碼由原作者 [TienYang](https://github.com/wy36101299) 製作並由 [Allen Chou](https://github.com/s3131212) 修改後釋出。

因為原專案最後一次更新已經是 2015 年初，之後中央氣象局更動了網站的結構，原本的 Code 不能沿用，故修改之。然而原作者帳號看來沒有在活動了，故拿來修到會運作並以獨立 repo 以 [MIT](https://github.com/s3131212/CWB-Observation-Crawler/blob/master/LICENSE) 釋出。