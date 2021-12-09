# Author: Wanying

import re
import sqlite3

punctuation = ':/'
def removePunctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation),'',text)
    return text.strip()

def createDatabase(deviceAddress, **kwargs):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    # print(databese)
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists SELFDATA
                    (SENSOR TEXT NOT NULL,
                    DATA TEXT NOT NULL,
                    TIMESTAMP TIMESTAMP NOT NULL)''')
    c.execute('''CREATE TABLE if not exists OTHERDATA
                    (ADDRESS TEXT NOT NULL, 
                    SENSOR TEXT NOT NULL,
                    DATA TEXT NOT NULL,
                    TIMESTAMP TIMESTAMP NOT NULL)''')
    conn.commit()
    conn.close()

def insertData(deviceAddress, sensor, data, timeStamp, **kwargs):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    if sensor == 'human':
        data = ','.join(data)
    c.execute("INSERT INTO SELFDATA(SENSOR,DATA,TIMESTAMP) VALUES (?,?,?)",(sensor, str(data), timeStamp))
    conn.commit()
    conn.close()

def insertOtherData(deviceAddress, address, sensor, data, timeStamp, **kwargs):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    if sensor == 'human':
        data = ','.join(data)
    c.execute("INSERT INTO OTHERDATA(ADDRESS,SENSOR,DATA,TIMESTAMP) VALUES (?,?,?,?)", (address, sensor, str(data), timeStamp))
    conn.commit()
    conn.close()

def selectDataAll(deviceAddress, **kwarg):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    result = c.execute("SELECT * from SELFDATA ORDER BY SENSOR").fetchall()
    conn.commit()
    conn.close()
    return result

def selectOtherDataAll(deviceAddress, **kwarg):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    result = c.execute("SELECT * from OTHERDATA ORDER BY ADDRESS,SENSOR").fetchall()
    conn.commit()
    conn.close()
    return result

def selectDataSummary(deviceAddress, **kwarg):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    result = c.execute("SELECT SENSOR, count(*) AS DataVolume from SELFDATA GROUP BY SENSOR").fetchall()
    conn.commit()
    conn.close()
    return result

def selectOtherDataSummary(deviceAddress, **kwarg):
    databese = 'data/' + removePunctuation(deviceAddress) + '.db'
    conn = sqlite3.connect(databese)
    c = conn.cursor()
    result = c.execute("SELECT ADDRESS, SENSOR, count(*) AS DataVolume from OTHERDATA GROUP BY ADDRESS,SENSOR ORDER BY ADDRESS").fetchall()
    conn.commit()
    conn.close()
    return result
