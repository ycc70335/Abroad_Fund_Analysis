import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
encoding = "utf-8"

#把資料抓下來:大專院校本國學生出國進修交流數 以 103學年度為例
url1 = "https://udb.moe.edu.tw/Home/FileDownload/STU_N070000_E03"

#由於原始連結只有ods檔案，故下載後用excel手動轉檔為csv檔
abroad_v1 = pd.read_csv("abroad103_2.csv") #讀取csv
school = abroad_v1.groupby("學校名稱") #照學校去group
x1 = school.get_group("國立臺灣大學")
y1 = sum(x1["小計"])
x2 = school.get_group("國立清華大學")
y2 = sum(x2["小計"])
x3 = school.get_group("國立交通大學")
y3 = sum(x3["小計"])
x4 = school.get_group("國立成功大學")
y4 = sum(x4["小計"])

x_abroad_v1 = ["NTU", "NTHU", "NCTU", "NCKU"] #[圖表1]台清交成的出國人數
y_abroad_v1 = [y1, y2, y3, y4] #這四間學校的出國人數sum

#[圖表1]長條圖
plt.figure(figsize=(10, 5))
plt.title('Students studying abroad')
for x,y in enumerate(y_abroad_v1):
    plt.text(x,y+10,'%s' %round(y,1),ha='center')
plt.bar(x_abroad_v1, y_abroad_v1, color='blue', width=0.5 , linestyle=':')
plt.show()


# 把資料抓下來:教育部補助全國大專校院經費 以 103學年度為例
url2 = 'https://quality.data.gov.tw/dq_download_csv.php?nid=14536&md5_url=6a11eaf495c8d084ea18409a264c79c1'
fund_v1 = pd.read_csv(url2) #讓url2的資料變成pandas的dataframe
fund_v1_2 = fund_v1.groupby("大專院校名稱")
x1 = fund_v1_2.get_group("國立臺灣大學")
x2 = fund_v1_2.get_group("國立清華大學")
x3 = fund_v1_2.get_group("國立交通大學")
x4 = fund_v1_2.get_group("國立成功大學")

#把經費中的逗號去掉，計算總額
def Split_comma(n):
    one_str = ""
    fund_sum = 0
    for i in range(len(n["補助經費"])):
        fund_split = str(n.iat[i, 3]).split(",")
        for j in range(len(fund_split)):
            one_str = one_str + fund_split[j]
        fund_sum = fund_sum + int(one_str)
        one_str = ""
    return fund_sum
y1 = Split_comma(x1)
y2 = Split_comma(x2)
y3 = Split_comma(x3)
y4 = Split_comma(x4)

#[圖表2]長條圖_各校補助經費:
x_fund_v1 = ["NTU", "NTHU", "NCTU", "NCKU"] #[圖表1]台清交成的出國人數
y_fund_v1 = [y1, y2, y3, y4] #這四間學校的出國人數sum

plt.figure(figsize=(10, 5))
plt.title('funding analysis')
for x,y in enumerate(y_fund_v1):
    plt.text(x,y+100,'%s' %round(y,1),ha='center')
plt.bar(x_fund_v1, y_fund_v1, color = 'lightblue', width = 0.5 , linestyle=':')
plt.show()

# 贊助與出國人數的相關係數
df = pd.DataFrame()
df["a"] = y_abroad_v1
df["b"] = y_fund_v1
print(df.corr()) #r=0.90094

#[圖表3]長條圖_以成功大學為例，補助經費類型與排名
#此處需要修改matplotlib的預設字體以便於表格內顯示中文
fund_ncku = x4.ix[:, ["補助計畫", "補助經費"]]
#需要先把逗號移除
for i in range(len(fund_ncku)):
    fund_ncku.iat[i,1] = fund_ncku.iat[i,1].replace(",", "") #將字串中的逗號移除
    fund_ncku.iat[i,1] = int(fund_ncku.iat[i,1]) #宣告字串為整數以便後續相加

fund_ncku_sum = fund_ncku.groupby("補助計畫").sum()
fund_ncku_sum_sorted = fund_ncku_sum.sort_values(by = "補助經費", ascending = False)

x_fund_ncku = []
y_fund_ncku = [] 
for i in range (5): #找到補助經費前五名
    x_fund_ncku.append(fund_ncku_sum_sorted.index[i])
    y_fund_ncku.append(fund_ncku_sum_sorted.iat[i,0])

plt.figure(figsize=(30, 20))
# 設置Y軸的刻度範圍
plt.ylim([150000,150000000])
# 為每個條形圖添加數值標籤
for x,y in enumerate(y_fund_ncku):
    plt.text(x,y+100,'%s' %round(y,1),ha='center')
plt.bar(x_fund_ncku, y_fund_ncku, color = 'steelblue', width = 0.5 ,  linestyle=':')
plt.title('Top funding items in NCKU')
plt.show()




