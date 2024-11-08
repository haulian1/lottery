from datetime import datetime

import os
import pytz
import random
import re as regex
import secrets as s
import shutil
import sys

# Check all arguments exist
if len(sys.argv) != 2:
	sys.exit(1)

# Assign arguments
MODE_TYPE = sys.argv[1]
LAST_WINNING_TICKET = sys.argv[2]

# Check argument validity
match MODE_TYPE.upper():
    case modes.MEGAMILLION_MODE:
        if not regex.match(r"([0][1-9]|[1-6][0-9]|70){5}([0-1][1-9]|[2][0-5])", LAST_WINNING_TICKET):
        	sys.exit(3)
    case modes.POWERBALL_MODE:
        if not regex.match(r"([0][1-9]|[1-6][0-9]){5}([0-1][1-9]|[2][0-5])", LAST_WINNING_TICKET):
        	sys.exit(4)
    case _:
    	sys.exit(5)

if len(LAST_WINNING_TICKET) != 12:
	sys.exit(2)

# Create constant classes and variables

class modes:
    POWERBALL_MODE = 'POWER'
    MEGAMILLION_MODE = 'MEGA'

TIME_ZONE = pytz.timezone("America/New_York")

BATCH_SIZE = 2000000

WHITE_POWER_BALL_LIMIT = 69
POWER_BALL_LIMIT = 26

WHITE_MEGA_BALL_LIMIT = 70
MEGA_BALL_LIMIT = 25

MEGAMILLION_DAY_OFFSETS = [(1,1), (0,3), (2,2), (1,1), (0,4), (3,3), (2,2)]
POWERBALL_DAY_OFFSETS = [(0,2), (1,1), (0,3), (2,2), (1,1), (0,2), (1,1)]

# Create global variables
FIND_LOTTO_FILES = []
PLAY_LOTTO_FILES = []

FIND_LOTTO_COMBINED = None
PLAY_LOTTO_COMBINED = None

FIND_TICKET = None
PLAY_TICKET = None

MAX_NUM_WHITE = WHITE_MEGA_BALL_LIMIT if MODE_TYPE == modes.MEGAMILLION_MODE else WHITE_POWER_BALL_LIMIT
MAX_NUM_SPECIAL = MEGA_BALL_LIMIT if MODE_TYPE == modes.MEGAMILLION_MODE else POWER_BALL_LIMIT

#  0 is Monday and 6 is Sunday
def get_days_offset(weekday, hr):
    if MODE_TYPE == modes.MEGAMILLION_MODE:
        offset = MEGAMILLION_DAY_OFFSETS[weekday]
        return offset[0] if hr < 23 else offset[1]
    elif MODE_TYPE == modes.POWERBALL_MODE:
        offset = POWERBALL_DAY_OFFSETS[weekday]
        return offset[0] if hr < 23 else offset[1]
    else:
        sys.exit(6)

def get_next_lotto_date():
	NOW = datetime.datetime.now(TIME_ZONE)
    days_offset = get_days_offset(NOW.weekday(), NOW.hour)
    
    next_lotto_date = NOW + timedelta(days=days_offset)
    return f"{next_lotto_date.year}_{next_lotto_date.month}_{next_lotto_date.day}"

NEXT_LOTTO_DATE = get_next_lotto_date()

# Create files and folders?
# Have the ability to generate numbers based on lotto type

def get_white_balls():
    nums = set([])
    while len(nums) < 5:
        num = s.randbelow(MAX_NUM_WHITE) + 1
        nums.add(num)
    return ''.join([str(x) if x >= 10 else '0' + str(x) for x in sorted(nums)])

def gen_special_ball():
    special = s.randbelow(MAX_NUM_SPECIAL) + 1
    return str(special) if special >= 10 else '0' + str(special)

def gen_ticket():
    return get_white_balls() + gen_special_ball()

def gen_batch(size=BATCH_SIZE):
	batch = []
    for i in range(size):
        batch.append(gen_ticket())
    return sorted(batch)

def write_batch_to_file(file_name, tickets):
	with open(file_name, 'w') as file:
		file.write('\n'.join(tickets))


def choose_ticket(num_completed_iterations, current_ticket, new_tickets):
	if current_ticket == None:
		return s.choice(new_tickets)
	else:
		total_new = len(new_tickets)
		total_tickets = num_completed_iterations + total_new
		
		new_ticket = s.choice(new_tickets)

		tickets = [current_ticket, new_ticket]
		prob_dist = [num_completed_iterations/total_tickets, total_new/total_tickets ]
		
		return random.choice(tickets, weights=prob_dist)[0]

FIND_LOTTO_FILE_PREFIX = f"{MODE_TYPE}_{NEXT_LOTTO_DATE}_find"

counter = 0
winning_iteration = 0

with open('find_ticket_evolution.txt', 'w') as find_ticket_file:
	while True:
		tickets = gen_batch()
		file_name = f"{FIND_LOTTO_FILE_PREFIX}_{counter}.txt"
		write_batch_to_file(file_name, tickets)
		FIND_LOTTO_FILES.append(file_name)

		FIND_TICKET = choose_ticket(counter * BATCH_SIZE, FIND_TICKET, tickets)
		find_ticket_file.write(f'Counter: {counter}, ticket: {FIND_TICKET}\n')
		if LAST_WINNING_TICKET in tickets:
			winning_iteration = counter * BATCH_SIZE + tickets.index(LAST_WINNING_TICKET) 
			break

def add_remaining_lines_to_file_in_batches(output_file, input_file):
	lines = input_file.getlines(BATCH_SIZE)
	while line != "":
		output_file.write(f'{lines}\n')
		lines = input_file.getlines(BATCH_SIZE)


#merge all batches into one single sorted batch
def merge_all_files(run, files):
	for index, batched_file in enumerate(files):
		cur_merged_file = f"temp_{run}_merge_{index}.txt"
		if run == 'play':
			PLAY_LOTTO_COMBINED = cur_merged_file
		if run == 'find':
			FIND_LOTTO_COMBINED = cur_merged_file
		if index == 0:
			shutil.copy(batched_file, cur_merged_file)
			continue
		else:
			last_merged_file = f"temp_{run}_merge_{index-1}.txt"
			with open(cur_merged_file, 'w') as merged_file, \
				open(last_merged_file, 'r') as last_file, \
				open(batched_file, 'r') as cur_file:
					
				last_file_line = last_file.readline()				
				cur_file_line = cur_file.readline()
				
				while True:
					if cur_file_line == "":
						merged_file.write(f'{last_file_line}\n')
						add_remaining_lines_to_file_in_batches(merged_file, last_file)
						break
					elif last_file_line == "":
						merged_file.write(f'{cur_file_line}\n')
						add_remaining_lines_to_file_in_batches(merged_file, cur_file)
						break
					else:
						if cur_file_line <= last_file_line:
							merged_file.write(f'{cur_file_line}\n')
							cur_file_line = cur_file.readline()
						else:
							merged_file.write(f'{last_file_line}\n')
							last_file_line = last_file.readline()
			os.remove(last_merged_file)

merge_all_files('find', FIND_LOTTO_FILES)

def uniq_count_merged_file(run):
	combined_file_name = FIND_LOTTO_COMBINED if run == 'find' else PLAY_LOTTO_COMBINED
	with open(combined_file_name, 'r') as combined_file, \
	    open(f'uniq_sorted_{run}.txt', 'w') as uniq_sorted_file:

	    counter = 1
	    prev_ticket = combined_file.readline()
	    curr_ticket = combined_file.readline()
	    while True:
	    	if curr_ticket == '':
	    		uniq_sorted_file.write(f'{counter} {prev_ticket}\n')
	    		break
	    	
	    	if prev_ticket == curr_ticket:
	    		counter += 1
	    	else:
	    		uniq_sorted_file.write(f'{counter} {prev_ticket}\n')
	    		counter = 1

	    	prev_ticket = curr_ticket
	    	curr_ticket = combined_file.readline()

uniq_count_merged_file('find')

# Generate n-number of lotto tockets
PLAY_LOTTO_FILE_PREFIX = f"{MODE_TYPE}_{NEXT_LOTTO_DATE}_play"
counter = 0

with open('play_ticket_evolution.txt', 'w') as play_ticket_file:
	while winning_iteration > 0:
		tickets = gen_batch(size=min(winning_iteration, BATCH_SIZE))
		
		file_name = f"{PLAY_LOTTO_FILE_PREFIX}_{counter}.txt"
		write_batch_to_file(file_name, tickets)
		PLAY_LOTTO_FILES.append(file_name)

		PLAY_TICKET = choose_ticket(counter * BATCH_SIZE, PLAY_TICKET, tickets)
		play_ticket_file.write(f'Counter: {counter}, ticket: {PLAY_TICKET}\n')
		winning_iteration -= BATCH_SIZE

merge_all_files('play', PLAY_LOTTO_FILES)

uniq_count_merged_file('play')

