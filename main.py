import json
import jsonschema
from jsonschema import SchemaError, ValidationError
import os
import logging

logging.getLogger(__name__)
logging.basicConfig(filename='logging.log', filemode='w',
                    format='%(levelname)s: [%(asctime)s] %(message)s')

EVENTS_PATH = 'task_folder/event'
SCHEMAS_PATH = 'task_folder/schema'


def open_files(path):
    new_data = []
    paths_ = os.listdir(path)
    for path_ in paths_:
        full_path = os.path.join(path, path_)
        with open(full_path) as file_:
            file_data = json.load(file_)
        if file_data:
            new_data.append({'path': full_path, 'json': file_data})
        else:
            logging.warning(f'Sorry, {full_path} cannot be valid json file.')
    return new_data


def validate_files(event, schema):
    try:
        jsonschema.validate(event['json'], schema['json'])
    except SchemaError as ex:
        logging.warning(f'''Schema {schema['path']} is not correct. The main reason: {ex.message}''')
    except ValidationError as ex:
        logging.warning(f'''Event {event['path']} is not validated by {schema['path']}. The main reason: {ex.message}.''')




def main():
    events = open_files(EVENTS_PATH)
    schemas = open_files(SCHEMAS_PATH)

    val = [[validate_files(event, schema) for event in events] for schema in schemas]

if __name__ == '__main__':
    main()
