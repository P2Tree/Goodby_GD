import sqlite3
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import uuid

from export import Exp

conn = sqlite3.connect('GD.db')
c = conn.cursor()
print("database Opened")

## read template
cursor = c.execute("SELECT * FROM ZGDNTEMPLATEITEM")
# for row in cursor:
#     print("zcreatedate: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row[6]))))
#     print("ztitle: " + str(row[8]))
#     print("===")

template = []
for row in cursor:
    template.append(str(row[8]))

print(template)

## read diary data
cursor = c.execute("SELECT * FROM ZGDNDIARY")
diarys = []
class Diary():
    def __init__(self, id, mood, date, time, weather, bookmark):
        self.id = id
        self.mood = mood
        self.date = date
        self.weather = weather
        self.time = time
        self.bookmark = bookmark
        self.content = "###### "
        if self.get_weather() != "":
            self.content += self.get_weather() + " | "
        if self.get_mood() != "":
            self.content += self.get_mood() + "\n"

    def set_content(self, content):
        self.content = self.content + "\n" + content

    def get_id(self):
        return self.id
    def get_mood(self):
        if self.mood == 'Angry':
            ret = "挺生气"
        elif self.mood == 'Happy':
            ret = "很开心"
        elif self.mood == 'Very Happy':
            ret = "非常开心"
        elif self.mood == 'Neutral':
            ret = "平常心"
        elif self.mood == "Wondering":
            ret = "困惑，想不通"
        elif self.mood == "Unhappy":
            ret = "不开心"
        elif self.mood == "Cool":
            ret = "自信，兴奋"
        elif self.mood == "Sad":
            ret = "伤心"
        else:
            ret = ""
        return ret
    def get_date(self):
        return self.date
    def get_time(self):
        return self.time
    def get_weather(self):
        if self.weather == 'Sun':
            ret = "天气晴朗"
        elif self.weather == 'Wind':
            ret = "刮大风"
        elif self.weather == 'Lightning':
            ret = "阳光明媚"
        elif self.weather == 'Fog':
            ret = "起雾了"
        elif self.weather == 'Rain':
            ret = "下大雨了"
        elif self.weather == 'Cloud':
            ret = "多云"
        elif self.weather == 'Drizzle':
            ret = "毛毛雨"
        elif self.weather == 'Snow':
            ret = "下雪了"
        else:
            ret = ""
        return ret
    def get_content(self):
        return self.content
    def get_bookmark(self):
        return self.bookmark
    def get_utc_datetime(self):
        date_time_stamp = datetime(year=int(self.date[0:4]), month=int(self.date[5:7]),\
                             day=int(self.date[8:]), hour=int(self.time[0:2]), \
                             minute=int(self.time[3:5]), second=int(self.time[7:]))
        utc_time_stamp = date_time_stamp - timedelta(hours=8)
        return str(utc_time_stamp.strftime("%Y-%m-%d")) + "T" + str(utc_time_stamp.strftime("%H:%M:%S")) + "Z"

    def __str__(self):
        s = "Id: " + str(self.id) + "\n"
        if self.mood:
            s = s + "Mood: " + self.mood + "\n"
        if self.date:
            s = s + "Date: " + self.date + "\n"
        if self.time:
            s = s + "time: " + self.time + "\n"
        if self.weather:
            s = s + "Weather: " + self.weather + "\n"
        if self.content:
            s = s + "Content: " + self.content
        if self.bookmark:
            s = s + "Bookmarked: " + str(self.bookmark)
        return s

for row in cursor:
    create_time = datetime.fromtimestamp(row[5])
    create_time_str = create_time.strftime("%H:%M:%S")
    #print("create time: " + create_time_str)
    # id, mood, date, time, weather, bookmark
    diarys.append(Diary(row[0], row[11], row[12], create_time_str, row[13], row[3]))

## read diary content
cursor = c.execute("SELECT * FROM ZGDNGRID")
not_matched = []
for row in cursor:
    #print("which diary: " + str(row[4]))
    #print("content: " + row[8])
    #print("title: " + row[9])
    #print("===")

    is_matched = False
    for d in diarys:
        if d.get_id() == row[4]:
            #print("diary matched: " + str(row[4]))
            is_matched = True
            if row[8] != "":
                contents = "#### " + row[9] + "\n" + row[8]
                d.set_content(contents)
            break
    if not is_matched:
        #print("not find diary: " + str(row[4]))
        not_matched.append(row[4])

if len(not_matched) != 0:
    print("not matched: ")
    print(not_matched)

#for item in diarys:
    #print("===")
    #print(item)

## Begin to export

exp = Exp("GridDiary.json")
dics = []

for item in diarys:
    if item.get_content() == "":
        continue
    tmp = {}
    tmp['editingTime'] = 0
    tmp['creationDeviceType'] = "MacBook Pro"
    tmp['modifiedDate'] = item.get_utc_datetime()
    tmp['tags'] = ["GridDiary", "ManualImport"]
    tmp['text'] = item.get_content()
    tmp['creationOSName'] = "macOS"
    tmp['creationDeviceModel'] = "MacBookPro13,3"
    if item.get_bookmark() == 1:
        tmp['starred'] = True
    else:
        tmp['starred'] = False
    tmp['creationDate'] = item.get_utc_datetime()
    tmp['creationOSVersion'] = "10.14.6"
    tmp['creationDevice'] = "韩会杰的MacBook Pro"
    tmp['uuid'] = str(uuid.uuid1()).replace('-', '').upper()
    tmp['timeZone'] = "Asia\/Shanghai"
    tmp['duration'] = 0

    dics.append(tmp)

exp.write(dics)