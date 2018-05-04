import csv
import subprocess
import time
from itertools import islice
from mongoengine import connect
from models import Entry

connect(
    db='gpu_usage',
    host='mongodb://gpu4:27017/cin_cluster'
)

while True:
    subprocess.call(['./shell/nvidia-smi.sh'], shell=True)
    with open('data/gpu.csv', 'r', encoding='utf-8') as csvfile:
        results = csv.reader(csvfile, delimiter=',')
        rows = islice(results, 1, None) # skip headers
        entries = [Entry.create(row) for row in rows]
        for entry in entries:
            print(entry)
            entry.save()
        time.sleep(5)
    
