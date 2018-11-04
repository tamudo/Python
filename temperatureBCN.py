from urllib import request as urlrequest
from bs4 import BeautifulSoup
import re
import time
import os.path
class TemperatureBCN:
    def __init__(self):
        self.hour = ''
        self.date = ''
        self.celsius = ''

    
    def get_data(self):
        proxy_support = urlrequest.ProxyHandler({})
        opener = urlrequest.build_opener(proxy_support)
        urlrequest.install_opener(opener)

        with urlrequest.urlopen('http://www.infomet.am.ub.es/metdata') as responset:
            response = (responset.read())
            soup = BeautifulSoup(response)

        data = soup.find_all('th')
        for link in data:
            if link.find(text=re.compile("Dades recollides")):
                self.hour = (link.text[23:28])
                self.date = (link.text[-8:])
                break

        links = soup.find_all('li')
        for link in links:
            if link.find(text=re.compile("Temperatura")):
                self.celsius = (link.text[-4:])
                break

    def to_file(self, file_dir):    
    
        if os.path.exists(file_dir):
            csv = open(file_dir, "a")     
        else:
            csv = open(file_dir, "w") 
            columnTitleRow = "Hour; Date; Celsius\n"
            csv.write(columnTitleRow)
        
        row = self.hour + ";" + self.date + ";" + self.celsius +"\n"
        csv.write(row)
        csv.close()

x =TemperatureBCN()
x.get_data()
x.to_file("BCNDegree.csv" )