import csv
import loginForm as lf
import pandas as pd
tampungUsers=[]
nama=''
idUser=''
def loadData():
    with open('biodata_customer.csv','r') as data:
        readFile=csv.reader(data,delimiter=',')
        next(readFile, None)
        for line in readFile:
            tampungUsers.append(line)
    return True
def login(username,password):
    usernm = username
    passwd = password
    for user in tampungUsers:
        if user[2] == usernm and user[3] == passwd:
                lf.nama=user[1]
                lf.idUser=user[0]
                return True
    else:
        return False

def getName():
        return nama
def getID():
        return idUser

loadData()
# login('gainiscoxia2p','jptaqz')
# print(getName())
# print(getID())
