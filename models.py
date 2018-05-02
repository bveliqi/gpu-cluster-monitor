import json
import socket
import datetime
import time
import os
from dateutil import parser as dateparser

from mongoengine import Document, IntField, ComplexDateTimeField, DateTimeField, StringField

class Entry(Document):

    meta = {
        'collection': 'gpu_usage',
        'indexes': [
            {
                'fields': ['timestamp'],
                'expireAfterSeconds': 7 * 24 * 60 * 60 # seven days
            }
        ]
    }

    index = IntField(required=True)
    host = StringField(required=True)
    unique_ID = StringField(required=True)
    timestamp = DateTimeField(required=True)
    name = StringField(required=True)
    temperature = IntField(required=True)
    utilization_gpu_percentage = IntField(required=True)
    utilization_memory_percentage = IntField(required=True)
    memory_total_mb = IntField(required=True)
    memory_free_mb = IntField(required=True)
    memory_used_mb = IntField(required=True)
    pstate = IntField(required=True)


    @staticmethod
    def create(row):
        '''
            Cleanse the data from CSV row and create mongoDB entry out of it
        '''
        entry = Entry()
        entry.index = row[0]
        entry.host = os.getenv('HOSTNAME', socket.gethostname())
        entry.unique_ID = "{0}_{1}".format(entry.host, entry.index)
        entry.timestamp = row[1].strip()
        entry.name = row[2].strip()
        entry.temperature = int(row[3].strip())
        entry.utilization_gpu_percentage = int(row[4].replace('%','').strip())
        entry.utilization_memory_percentage = int(row[5].replace('%','').strip())
        entry.memory_total_mb = int(row[6].replace('MiB','').strip())
        entry.memory_free_mb = int(row[7].replace('MiB','').strip())
        entry.memory_used_mb = int(row[8].replace('MiB','').strip())
        entry.pstate = int(row[9].replace('P', '').strip())
        return entry

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return "host: {0} - index {1} - gpu [%]: {2} - memory [%]: {3}".format(self.host, self.index, self.utilization_gpu_percentage, self.utilization_memory_percentage)