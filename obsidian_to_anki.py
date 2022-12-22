import re
import csv
import sys
import os
from datetime import datetime
import logging

import global_data
import add_question_object

################### SET UP ###########################
obsidian_path = "" # the absolute path to your obsidian vault

root_folder_path = "" # the absolute path to the folder containing this script
################ END OF SET UP #######################

file_names = input()  # not case sensitive
global_data.input_files = list(file_names.split(", "))

# set up log folder for this run
current_time = datetime.now()
today = "{:d}_{:02d}_{:02d}-{:02d}-{:02d}-{:02d}".format(
    current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second)
log_folder_path = root_folder_path + "/logs/" + today + "/"
output_csv_path = root_folder_path + "/outputs/" + today + "/"


# Creates an output csv with questions and answers formatted in csv style
def make_output_csv(file_name, questions):
    try:
        keys = questions[0].keys()
        with open(output_csv_path + file_name + '.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writerows(questions)
        logging.info("output csv has been written, path at " + output_csv_path)
    except:
        logging.error("unable to print output csv")

# Check if output dir exists
if not os.path.exists(output_csv_path):
    os.makedirs(output_csv_path)

if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

for file_name in global_data.input_files:
    logging.basicConfig(filename=log_folder_path + file_name + ".log", encoding='utf-8', level=logging.DEBUG,)
    questions = []
    if "|" in file_name:
        file_name = file_name.split("|")[0]
    path = ""
    for root, dirs, files in os.walk(obsidian_path):
        if str(file_name + ".md") in files:
            path = os.path.join(root, file_name + ".md")
    if path == "":
        logging.error("ERROR: " + file_name + ".md was not found in the files")

    # open file contents
    try:
        logging.info("trying to open: " + path + " with filename: " + file_name)
        file = open(path)
        text = file.read()
    except:
        logging.error("unsuccessful file read")
        sys.exit()

    # ignore metadata and anything above
    if "---" in text:
        text = text.split("---")[2]

    # split text into lines
    lines = text.split("\n")

    # remove everything before title
    # for line in list(lines):
    #     if "#" not in line:
    #         lines.remove(line)
    #     else:
    #         break

    size = len(lines)

    # Find all links
    linked_files = re.findall(r'\[\[(.*?)\]\]', ''.join(lines))

    logging.info("links in file:")
    logging.info(linked_files)

    for link in linked_files:
        if not link.endswith('.png'):
            if link not in global_data.input_files:
                global_data.input_files.append(link)

    # only print "valid question" lines
    # {text: "", answers: []}
    for i in range(size):
        line = lines[i].strip()
        # Check for and handle code
        if '```' in line:
            if global_data.current_line_type == "code":
                global_data.current_line_type = ""
                continue
            else:
                global_data.current_line_type = "code"
                continue

        if global_data.current_line_type == "code":
            continue
        # If line is not empty and doesn't start with - (answer format)
        if line != '' and line[0] != '-' and line[0] != '#':
            # If valid question
            if line.endswith('?'):
                # Check for inline latex in question
                line = re.sub('\$\$([^$]*)\$\$', '\\[\g<1>\\]', line)
                line = re.sub('\$(\S[^$]*\S)\$', '\\(\g<1>\\)', line)

                # Check for inline code in question
                line = re.sub(
                    '`(.*?)`', r'<code class="code code-inline">\1</code>', line)

                logging.info(f'\n\nQuestion: {line}\n')
                output = add_question_object.add_question_object(
                    line, lines, i, file_name)
                questions.append(output)
    make_output_csv(file_name, questions)

logging.info("checked files:")
logging.info(global_data.input_files)
