import datetime
import dateutil.relativedelta
from pymongo import MongoClient
from prettytable import PrettyTable
from termcolor import colored, cprint


client = MongoClient('mongodb://gpu4:27017/')
db = client['cin_cluster']
gpus = db['gpu_usage']


def query_mongodb():
    '''
        Get timestsamp for last usage (i.e. utilization > 0%) for every GPU in the cluster
    '''
    results = gpus.aggregate(
        [
            { '$sort': { 'timestamp': 1} },
            { '$match': {'utilization_gpu_percentage' : { '$gt' : 0}}},
            {
            '$group':
                {
                '_id': "$unique_ID",
                'timestamp': { '$last': "$timestamp" },
                'index': { '$last': "$index" },
                'host': { '$last': "$host" },
                'unique_ID': { '$last': "$unique_ID" },
                'name': { '$last': "$name" },
                'utilization_gpu_percentage': { '$last': "$utilization_gpu_percentage" },
                'utilization_memory_percentage': { '$last': "$utilization_memory_percentage" },
                'memory_total_mb': { '$last': "$memory_total_mb" },
                'memory_free_mb': { '$last': "$memory_free_mb" },
                'memory_used_mb': { '$last': "$memory_used_mb" },
                'temperature': { '$last': "$temperature" },
                'pstate': { '$last': "$pstate" },
                'host': { '$last': "$host" }               
                }
            }
        ]
        )
    return results


def pretty_time_diff(date):
    now = datetime.datetime.utcnow()
    delta = dateutil.relativedelta.relativedelta (now, date)
    if delta.days > 0:
        return "%dd %dh %dm %ds" % (delta.days, delta.hours, delta.minutes, delta.seconds)
    if delta.hours > 0:
        return "%dh %dm %ds" % (delta.hours, delta.minutes, delta.seconds)
    if delta.minutes > 0:
        return "%dm %ds" % (delta.minutes, delta.seconds)


def free_gpus():
    '''
        Finds GPUs that have not been used for more than 1h
    '''
    results = query_mongodb()
    for result in results:
        last_used = result['timestamp']
        now = datetime.datetime.utcnow()
        diff = abs((now - last_used).total_seconds() / 60.0)
        if diff > 60.0:
            yield result


def add_row_to_table(table, gpu):
        free_since = colored(pretty_time_diff(gpu['timestamp']), 'yellow', attrs=['reverse'])
        name = gpu['name']
        host = colored(gpu['host'], 'blue', attrs=['reverse'])
        index = colored(gpu['index'], 'blue', attrs=['reverse'])
        table.add_row([free_since, name, host, index])


if __name__ == '__main__':
    free_gpus = free_gpus()
    print()
    table = PrettyTable(['Free Since', 'Name', 'Host', 'GPU'])
    for gpu in free_gpus:
        add_row_to_table(table, gpu)
    print(table)
    print()
