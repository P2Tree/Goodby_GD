import json
import os

class Exp():
    def __init__(self, name):
        self.filename = name
        self.header = open(name, 'w')
        print("Write to " + self.header.name)

    def exp_item(self, dics):
        self.header.write("\n  ")
        json.dump(dics[0], self.header)
        for d in dics[1:]:
            self.header.write(",")
            self.header.write("\n  ")
            json.dump(d, self.header)

    def exp_body(self, dics):
        self.header.write("\n\"entries\" : [")
        self.exp_item(dics)
        self.header.write("\n]")

    def exp_metadata(self):
        self.header.write("\n\"metadata\" : {")
        self.header.write("\n  \"version\" : 1.0")
        self.header.write("\n}")

    def write(self, dics):
        self.header.write("{")
        self.exp_metadata()
        self.header.write(",")

        self.exp_body(dics)
        self.header.write("\n}")

        self.header.close()

if __name__ == "__main__":
    exp = Exp("Diary.json")
    dics = []

    tmp = {}
    tmp['tags'] = "GridDiary"
    tmp['text'] = "luckily1"
    dics.append(tmp)

    tmp = {}
    tmp['tags'] = "GridDiary"
    tmp['text'] = "luckily2"
    dics.append(tmp)

    exp.write(dics)
