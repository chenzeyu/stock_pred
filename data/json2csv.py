import json
import csv
from pprint import pprint
import sys
import os
import os.path
import shutil

#jsonfiles = ['tsla.json']
jsonfiles = ['aapl.json','twtr.json','tsla.json','goog.json']

for jsonfile in jsonfiles:
    
    path = os.path.join(os.path.dirname(__file__), jsonfile)
    pathcsv = os.path.join(os.path.dirname(__file__), jsonfile.replace('.json','.csv'))
    
    with open(path) as data_file, open(pathcsv, 'w') as csvfile:    
        data = json.load(data_file)
    
        fieldnames = ['firstpost_date', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for datum in data:
            date = datum['firstpost_date']
            content = datum['content']
            writer.writerow({'firstpost_date': str(date), 'content': content.encode('utf-8')})
