from __future__ import print_function

import json
import imp
import os
import requests
import functools

import params  # This module is generated before this script is run

result_obj = {
    'timeout': 0.0,
    'error': None
}

result_path = os.path.join(os.environ['OUTPUT_DIR'],
                           'result.json')

def write_path(path, content):
    with open(path, 'w') as out:
        out.write(content)

write_result = functools.partial(write_path, result_path)

try:
    response = requests.post(params.url,
                            headers={'Authentication': 'Bearer {}'
                            .format(params.token)})
except Exception as e:
    result_obj['error'] = str(e)
else:
    # if response.status_code != requests.codes.ok:
    # response.raise_for_status()
    result_obj['timeout'] = response.elapsed.total_seconds()
    
write_result(json.dumps(result_obj))
