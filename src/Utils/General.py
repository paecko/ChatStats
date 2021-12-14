from datetime import datetime

def unix_time_to_date_time_string(unix_timestamp):
    # divide unixTimestamp by 1000 as Siginal data timestamp is given in milliseconds
    date_time_string = datetime.fromtimestamp(unix_timestamp/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    return date_time_string

def are_required_parameters_in_message(message, required_parameters):
    for parameter in required_parameters:
        if parameter not in message:
            return False
    return True

def create_value_formatters(number_of_values):
    res = "?," * number_of_values
    return res[:-1]

def sort_by_second(elem):
    return elem[1]