import sys
import requests
from datetime import datetime, timedelta
import csv

Type = sys.argv[1] if len(sys.argv) > 1 else print("No energy type specified")  # must be "gas" or "electricity"
MAC = sys.argv[2] if len(sys.argv) > 1 else print("No IHD MAC address specified")
section_date = datetime(2021, 10, 1)

headers = {'Authorization': MAC}  # AUTH is my MAC code
url = "https://consumer-api.data.n3rgy.com/" + str(Type) + "/consumption/1/"
count = 0


def add90days(ssd):
    new_date = ssd + timedelta(days=90)
    return new_date


data_file = open("C:\\Users\\ash26\Desktop\\" + Type + "EnergyData.csv", 'w', newline='')
csv_writer = csv.writer(data_file)

while section_date.date() < datetime.now().date():
    query = '?start=' + section_date.strftime('%Y') + section_date.strftime('%m') + section_date.strftime('%d') + \
            '0000&end=' + add90days(section_date).strftime('%Y') + add90days(section_date).strftime('%m') + \
            add90days(section_date).strftime('%d') + '0000'
    api_url = url + query
    r = requests.get(url=api_url, headers=headers)

    for x in r.json()['values']:
        if count == 0:
            header = x.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow((x.values()))

    section_date = add90days(section_date)

data_file.close()
