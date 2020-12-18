import sqlite3
import time

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
diary = []
class Diary():
    def __init__(self, mood, date, weather):
        self.mood = mood;
        self.date = date;
        self.weather = weather;

    def get_mood(self):
        return self.mood
    def get_date(self):
        return self.date
    def get_weather(self):
        return self.weather
    def print

for row in cursor:
    print("mood: " + row[11])
    print("date: " + row[12])
    print("weather: " + row[13])
    print("===")
    diary.append(Diary(row[11], row[12], row[13]))

for item in diary:
    print(str(item.get_mood()) + str(item.get_date))