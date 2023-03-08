#Write a script that imports the files Baselight_export.txt & Xytech.txt using argparse
#parse (analyze) the data
#Compute data to export correct data
#export the data as csv file

#importing argparse and csv cause we need it
import argparse
from tabulate import tabulate

# Define command-line arguments
parser = argparse.ArgumentParser(description='Write data from two text files to a CSV file')
parser.add_argument('xytech_file', type=str, help='Path to the Xytech text file')
parser.add_argument('baselight_file', type=str, help='Path to the Baselight Export text file')
parser.add_argument('-o', '--output', type=str, help='Path to the output file (default: output.csv)', default='output.csv')

# Parse the command-line arguments
args = parser.parse_args()

# Read data from the Xytech text file
with open(args.xytech_file, 'r') as f1:
    xytech_data = f1.read()

# Read data from the Baselight Export text file
with open(args.baselight_file, 'r') as f2:
    baselight_data = f2.read()

# Extract information from the Xytech text file
producer = xytech_data.split('Producer: ')[1].split('\n')[0].strip()
operator = xytech_data.split('Operator: ')[1].split('\n')[0].strip()
job = xytech_data.split('Job: ')[1].split('\n')[0].strip()
notes = xytech_data.split('Notes:\n')[1].strip()
location = xytech_data.split('Location:\n')[1].strip()

# Create a dictionary that maps file paths to frame numbers
frame_dict = {}
for line in baselight_data.split('\n'):
    parts = line.split(' ', 1)
    if len(parts) > 1:
        frames = []
        for frame in parts[1].split():
            if frame.isdigit():
                frames.append(int(frame))
        if len(frames) > 0:
            if parts[0] not in frame_dict:
                frame_dict[parts[0]] = frames
            else:
                frame_dict[parts[0]].extend(frames)

# Convert frame numbers to ranges
def convert_to_ranges(frame_list):
    frame_list = sorted(set(frame_list))
    ranges = []
    start = frame_list[0]
    end = frame_list[0]
    for i in range(1, len(frame_list)):
        if frame_list[i] == end + 1:
            end = frame_list[i]
        else:
            ranges.append((start, end))
            start = frame_list[i]
            end = frame_list[i]
    ranges.append((start, end))
    return ranges


# Create a table to display the data
#line 1 | producer name | operator | job | Notes
#line 4 | show location | frames to fix| (if frames are consecutive, show in ranges)
table_data = [    ['Producer', 'Operator','Job', 'Notes', 'Fames to Fix'],
                  [producer, operator, job, notes],['']]

table = tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid')
for file_path in frame_dict.keys():
    ranges = convert_to_ranges(frame_dict[file_path])
    frames = ' '.join([f"{start}-{end}" if start != end else str(start) for start, end in ranges])
    row = [file_path, '', '', '', frames]
    table_data.append(row)

headers = ['', '', '', '', '']
tablefmt = 'grid'
table = tabulate(table_data, headers=headers, tablefmt=tablefmt).replace(',', '')

# Write the table to a CSV file
with open(args.output, 'w', newline='') as f:
    f.write(table)

