from MessageDatabase import MessageDatabase
from . import General


def load_database(message_database, json_obj):
    for message in json_obj:
        if are_required_parameters_in_message(message):
            timestamp_string = General.unix_time_to_date_time_string(message['timestamp'])
            extracted_message_data = (timestamp_string, message['sourceUuid'], message['body'], message['conversationId'])
            message_database.insert(extracted_message_data)
    message_database.close_connection()


def are_required_parameters_in_message(message):
    required_parameters = MessageDatabase.get_required_parameters()
    for parameter in required_parameters:
        if parameter not in message:
            return False
    return True

