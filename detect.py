import os
from datetime import datetime, date
    

def scan_date(timestamp, date_obj):
    x = datetime(year=date_obj.year, month=date_obj.month, day=date_obj.day)
    d = datetime.utcfromtimestamp(timestamp)
    if d < x:
        return True


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formatted_date = d.strftime('%d-%m-%Y')

    return formatted_date


def update_trv(rows, trv):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)



def simple_scan(filepath, date_obj, trv):
    trv.delete(*trv.get_children())
    for entry in os.scandir(filepath):
        if entry.is_dir():
            # print(entry.path)
            # path = str(entry.path)
            # new_path = path.replace('\\', '/')
            simple_scan_to(entry, date_obj, trv)
        else:
            info =  entry.stat()
            mod_date = info.st_mtime
            if scan_date(info.st_mtime, date_obj):
                file_name = entry.name
                filesize = str(round(info.st_size/1000000, 3)) + 'mb'
                # print(entry.path + " : "+ convert_date(mod_date))
                details = (file_name, filesize, convert_date(mod_date), entry.path)
                trv.insert('', 'end', values=details)

def simple_scan_to(filepath, date_obj, trv):
    for entry in os.scandir(filepath):
        if entry.is_dir():
            # print(entry.path)
            # path = str(entry.path)
            # new_path = path.replace('\\', '/')
            simple_scan(entry, date_obj, trv)
        else:
            info =  entry.stat()
            mod_date = info.st_mtime
            if scan_date(info.st_mtime, date_obj):
                file_name = entry.name
                filesize = str(round(info.st_size/1000000, 3)) + 'mb'
                # print(entry.path + " : "+ convert_date(mod_date))
                details = (file_name, filesize, convert_date(mod_date), entry.path)
                trv.insert('', 'end', values=details)
                






