import os

import helpers as h
import secrets as s
import constants as c

def remove_empty_spaces(file: str) -> None:
    temp_file_name = f'temp_remove_empty_{s.randbelow(c.BATCH_SIZE*1000)}.txt'
    with open(file, 'r') as original_file,\
        open(temp_file_name, 'w') as temp_file:
        cur_lines = original_file.readlines(c.BATCH_SIZE)
        while len(cur_lines) > 0:
            next_lines = original_file.readlines(c.BATCH_SIZE)
            if len(next_lines) == 0:
                cur_lines[-1] = cur_lines[-1].rstrip('\n')
            temp_file.write(''.join(cur_lines))
            cur_lines = next_lines
    os.rename(temp_file_name, file)

