################################################################################
#   Takes all of the JSON files in a directory and compiles them into a single #
#   large JSON file.                                                           #
#                                                                              #
#   Written by: Jeremy Heckt, Let's Eat Labs - Scientist                       #
#   July, 2020, LC, Seattle, WA                                                #
################################################################################

import json
import os
import sys
import datetime


output_file_name = f"{str(datetime.datetime.now()).replace(' ', '_')}.json"
target_dir = f"{sys.argv[1]}/"
existing_json = os.listdir(target_dir)

total_files = 0

large_obj = {}

for f in existing_json:
    loaded_file = open(f"{target_dir}{f}").read()
    json_obj = json.loads(loaded_file)

    large_obj[total_files] = json_obj
    total_files += 1

with open(output_file_name, "w") as j:
    j.write(json.dumps(large_obj))
