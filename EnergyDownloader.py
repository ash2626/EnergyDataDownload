import sys
import requests
from datetime import datetime, timedelta
import mysql
from mysql.connector import errorcode

MAC = sys.argv[6] if len(sys.argv) > 1 else print("No IHD MAC address specified")
Type = sys.argv[7] if len(sys.argv) > 1 else print("No energy type specified")  # must be "gas" or "electricity"
section_date = datetime(2021, 10, 1)
headers = {'Authorization': sys.argv[6]}  # AUTH is my MAC code
url = "https://consumer-api.data.n3rgy.com/" + sys.argv[7] + "/consumption/1/"

def createDBconnection():
    try:
        cnx = mysql.connector.connect(user=sys.argv[1], password=sys.argv[2],
                                host=sys.argv[3],
                                port=int(sys.argv[4]),
                                database=sys.argv[5])
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            exit()
        else:
            print(err)
            exit()
    else:
        return cnx

def executeSQL(statement, cur):
  
  try:
    cur.execute(f"{statement}")
  
  except mysql.connector.Error as err:
    print(err) 

def add90days(ssd):
    new_date = ssd + timedelta(days=90)
    return new_date

cnx = createDBconnection()
cur = cnx.cursor()

cur.execute(f"CREATE DATABASE IF NOT EXISTS energy;")
cur.execute(f"CREATE TABLE IF NOT EXISTS gas (id INT auto_increment, timestamp TIMESTAMP, energy_usage FLOAT, primary key (id) );")
cur.execute(f"CREATE TABLE IF NOT EXISTS electricity (id INT auto_increment, timestamp TIMESTAMP, energy_usage FLOAT, primary key (id) );")

while section_date.date() < datetime.now().date():
    query = '?start=' + section_date.strftime('%Y') + section_date.strftime('%m') + section_date.strftime('%d') + \
            '0000&end=' + add90days(section_date).strftime('%Y') + add90days(section_date).strftime('%m') + \
            add90days(section_date).strftime('%d') + '0000'
    api_url = url + query
    print(api_url)
    r = requests.get(url=api_url, headers=headers)

    for x in r.json()['values']: 
        data=(x["timestamp"], x["value"])
        cur.execute("""INSERT INTO """+Type+""" (timestamp, energy_usage) values (%s, %s);""",data)
        cnx.commit()

    section_date = add90days(section_date)

cur.close()
=======
import sys
import requests
from datetime import datetime, timedelta
import csv
import os
import mysql
from mysql.connector import errorcode


Type = sys.argv[1] if len(sys.argv) > 1 else print("No energy type specified")  # must be "gas" or "electricity"
MAC = sys.argv[2] if len(sys.argv) > 1 else print("No IHD MAC address specified")
section_date = datetime(2021, 10, 1)

headers = {'Authorization': MAC}  # AUTH is my MAC code
url = "https://consumer-api.data.n3rgy.com/" + str(Type) + "/consumption/1/"
count = 0


def add90days(ssd):
    new_date = ssd + timedelta(days=90)
    return new_date


data_file = open(os.environ['USERPROFILE'] + "\Desktop\\" + Type + "EnergyData.csv", 'w', newline='')
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
