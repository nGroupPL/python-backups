import datetime

tmp_log = []


def log(s, end='\n'):
    s = datetime.datetime.now().strftime("%H:%M:%S") + ": " + s
    print(s, end=end)
    tmp_log.append(s)
