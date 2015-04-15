import json
import csv
from pprint import pprint
import sys
import os
import os.path
import shutil
import datetime

#jsonfiles = ['tsla.json']
jsonfiles = ['aapl.json','twtr.json','tsla.json','goog.json']

for jsonfile in jsonfiles:
    
    path = os.path.join(os.path.dirname(__file__), jsonfile)
    pathcsv = os.path.join(os.path.dirname(__file__), jsonfile.replace('.json','.csv'))
    
    with open(path) as data_file, open(pathcsv, 'w') as csvfile:    
        data = json.load(data_file)
    
        fieldnames = ['firstpost_date', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        
        writer.writeheader()
        for datum in data:
            timestamp = datum['firstpost_date']
            date = datetime.datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")
            
            content = datum['content']
            if (timestamp is not None) and (timestamp):
                writer.writerow({'firstpost_date': str(date), 'content': content.encode('utf-8').replace('\n', ' ').replace('\r', '')})