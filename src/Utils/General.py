from datetime import datetime

def unix_time_to_date_time_string(unix_timestamp):
    # divide unixTimestamp by 1000 as Siginal data timestamp is given in milliseconds
    date_time_string = datetime.fromtimestamp(unix_timestamp/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    return date_time_string