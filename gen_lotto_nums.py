import os
import re
import shutil
import sys

import helpers as h

try:
    print(sys.argv)
    _, lotto_type, last_winning_ticket = sys.argv
except:
    sys.exit(h.get_exit_status('invalid_args'))

print(f'reassign lotto_type')
lotto_type = h.validate_lotto_type(lotto_type)
print(f'lotto type is: {lotto_type}\n')


print(f'Validate lotto ticket')
h.validate_lotto_ticket(lotto_type, last_winning_ticket)
print(f'SUCCESS!\n')

print(f'get next lotto date')
next_lotto_date = h.get_next_lotto_date(lotto_type)
print(f'Next lotto date is : {next_lotto_date}\n')

# get current directory
# create directories
# change directory
# create files in new directory

print(f'find last winning ticket\n')
found_iteration, find_files = h.find_lotto_ticket(lotto_type, last_winning_ticket, next_lotto_date)
print(f'iteration: {found_iteration}')
print(f'find files: {find_files}\n')

combined_find_file_name = f'find_{next_lotto_date}_combined.txt'
print(f'combines file name: {combined_find_file_name}\n')

uniq_combined_find_file_name = f'uniq_{combined_find_file_name}'
print(f'uniq combined file name: {uniq_combined_find_file_name}\n')

print(f'merging sorted batch files \n')
h.merge_sorted_batch_files(find_files, combined_find_file_name, True)

print(f'generating uniq combined file \n')
h.count_uniq_lines(combined_find_file_name, uniq_combined_find_file_name)

print(f'gen numbers based on iter\n')
play_files = h.gen_lotto_ticket(lotto_type, found_iteration, next_lotto_date)

print(f'play files: {play_files}\n')
combined_play_file_name = f'play_{next_lotto_date}_combined.txt'

print(f'combined play files: {combined_find_file_name}\n')
uniq_combined_play_file_name = f'uniq_{combined_play_file_name}'
print(f'uniq combined play file {uniq_combined_play_file_name}\n')

print(f'merging sorted play files\n')
h.merge_sorted_batch_files(play_files, combined_play_file_name, True)

print(f'generating uniq combined file\n')
h.count_uniq_lines(combined_play_file_name, uniq_combined_play_file_name)

print(f'moving files')

new_dir = f'{lotto_type}_{next_lotto_date}'
os.mkdir(new_dir)

files = [x for x in os.listdir('.') if re.search(next_lotto_date, x)]
for file in files:
    shutil.move(file, new_dir)

print(f'ALL DONE')