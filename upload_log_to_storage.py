import os, pytz
from storage import Storage
from datetime import datetime, timedelta

storage = Storage()

def upload_log():
    today_log = 'hermes_us_{}.log'.format(datetime.now(pytz.timezone('US/Pacific')).strftime('%Y%m%d'))
    log_dir = '{}/log/'.format(os.path.dirname(os.path.realpath(__file__)))
    for log_name in os.listdir(log_dir):
        if log_name >= today_log:
            continue
        source = '{}/{}'.format(log_dir, log_name)
        storage.upload_log(source, log_name)
        os.remove(source)

# Removes logs that are created at or before gap_days ago.
def remove_old_logs(gap_days):
    date = datetime.now(pytz.timezone('US/Pacific')).strftime('%Y%m%d') - timedelta(days=gap_days)
    earlist_log = 'hermes_us_{}.log'.format(date)
    for log in storage.list_logs():
        if log < earlist_log:
            storage.delete_log(log)

if __name__ == '__main__':
    gap_days = 30
    remove_old_logs(gap_days)

    upload_log()
