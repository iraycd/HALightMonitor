import requests
import json
import datetime

class WonderwareOnline:
    def __init__(cls, address):
        cls.address = address

    def send_csv(self, authHeader, csvPayload):
        headers = {'Authorization': authHeader}
        r = requests.post(self.address + '/apis/upload/datasource',data=csvPayload, headers = headers)
        r.close()


class WonderwareOnlineCSV:
    def __init__(self):
        self.headers = ['datetime']
        self.row = [datetime.datetime.now().isoformat() + 'Z']

    def add_value(self, tagname, value):
        self.headers.append(tagname)
        self.row.append(value)

    def build(self):
        csvText = ''
        hIndex = 0
        for header in self.headers:
            csvText += str(header)
            hIndex += 1
            if hIndex != len(self.headers):
                csvText +=','
            

        csvText += '\n'

        rIndex = 0
        for item in self.row:
            csvText += str(item)
            rIndex += 1
            if rIndex != len(self.row):
                csvText += ','

        return csvText
