import copy
import os
import random
import re
import secrets as s
import shutil
import sys
import time
from datetime import datetime, timedelta
from multiprocessing import Process

import math

import constants as c

CPU_COUNT = os.cpu_count()


def get_exit_status(error_key: str) -> int:
    return c.Error.EXIT_STATUS[error_key]


def validate_lotto_type(lotto_type: str) -> str:
    match lotto_type.upper():
        case c.Modes.POWERBALL:
            return c.Modes.POWERBALL
        case c.Modes.MEGAMILLION:
            return c.Modes.MEGAMILLION
        case _:
            sys.exit(c.Error.EXIT_STATUS['assign_mode'])


def validate_lotto_ticket(lotto_type: str, lotto_ticket: str) -> bool:
    match lotto_type.upper():
        case c.Modes.MEGAMILLION:
            return bool(re.match(c.Regex.MEGAMILLION, lotto_ticket))
        case c.Modes.POWERBALL:
            return bool(re.match(c.Regex.POWERBALL, lotto_ticket))
        case _:
            sys.exit(c.Error.EXIT_STATUS['validate_lotto_ticket'])


def gen_single_number(limit: int) -> int:
    return s.randbelow(limit) + 1


def gen_batch_numbers(limit: int, batch_size: int) -> list[int]:
    return [gen_single_number(limit) for _ in range(batch_size)]


def get_days_offset(lotto_type: str, cur_week_day: int, cur_hr: int) -> int:
    if lotto_type == c.Modes.POWERBALL:
        day_offset_before_23, day_offset_after_23 = c.Power.DAY_OFFSETS[cur_week_day]
        return day_offset_before_23 if cur_hr < 23 else day_offset_after_23
    elif lotto_type == c.Modes.MEGAMILLION:
        day_offset_before_23, day_offset_after_23 = c.Mega.DAY_OFFSETS[cur_week_day]
        return day_offset_before_23 if cur_hr < 23 else day_offset_after_23
    sys.exit(c.Error.EXIT_STATUS['get_days_offset'])


def get_next_lotto_date(lotto_type: str, dt=datetime.now(c.DateTime.TIME_ZONE)) -> str:
    days_offset = get_days_offset(lotto_type, dt.weekday(), dt.hour)
    new_date = dt + timedelta(days=days_offset)
    return f'{new_date.year}_{new_date.month}_{new_date.day}'


def gen_ticket(lotto_type: str) -> str:
    white_limit = None
    special_limit = None
    if lotto_type == c.Modes.MEGAMILLION:
        white_limit = c.Mega.WHITE_BALL_LIMIT
        special_limit = c.Mega.SPECIAL_BALL_LIMIT
    elif lotto_type == c.Modes.POWERBALL:
        white_limit = c.Power.WHITE_BALL_LIMIT
        special_limit = c.Power.SPECIAL_BALL_LIMIT
    else:
        sys.exit(c.Error.EXIT_STATUS['gen_ticket'])

    nums = set([])
    cur_length = len(nums)
    while cur_length < 5:
        nums.update(gen_batch_numbers(white_limit, 5 - cur_length))
        cur_length = len(nums)
    white_balls = ''.join([f'{num}' if num >= 10 else f'0{num}' for num in sorted(nums)])

    num = gen_single_number(special_limit)
    num = f'{num}' if num >= 10 else f'0{num}'

    return f'{white_balls}{num}'


def gen_batch_tickets(lotto_type: str, batch_size=c.BATCH_SIZE) -> list:
    batch = []
    for index in range(batch_size):
        batch.append(gen_ticket(lotto_type))
    return sorted(batch)


def write_batch_to_file(file_name: str, tickets: list) -> None:
    with open(file_name, 'w') as output_file:
        output_file.write('\n'.join(tickets))
    return


def split_files(files: list) -> (list, list):
    if len(files) % 2 == 0:
        cur_queue = files
        new_queue = []
    else:
        cur_queue = files[:-1]
        new_queue = [files[-1]]
    return cur_queue, new_queue


def format_last_ele(ticket: str) -> str:
    return ticket if ticket[-1] == '\n' else f'{ticket}\n'


def copy_contents(source_file, dest_file) -> None:
    line = source_file.readlines(c.BATCH_SIZE)
    while True:
        if len(line) == 0:
            break
        else:
            dest_file.write(''.join(line))
            line = source_file.readlines(c.BATCH_SIZE)
    return


def merge_two_sorted_files(file1: str, file2: str, output_file_name: str) -> None:
    with open(file1, 'r') as left_file, \
            open(file2, 'r') as right_file, \
            open(output_file_name, 'w') as output_file:
        left_line = left_file.readline()
        right_line = right_file.readline()
        while True:
            if left_line == '':
                output_file.write(f'\n{right_line}')
                copy_contents(right_file, output_file)
                break
            if right_line == '':
                output_file.write(f'\n{left_line}')
                copy_contents(left_file, output_file)
                break
            if left_line < right_line:
                output_file.write(left_line)
                left_line = left_file.readline()
            else:
                output_file.write(right_line)
                right_line = right_file.readline()
    return


def delete_file(file: str) -> None:
    os.remove(file)
    return


def delete_files(files_to_delete: list) -> None:
    for file in files_to_delete:
        delete_file(file)
    return


def get_sigmoid_sleep_seconds(time_step: int, rate=0.01, max_limit=100, offset=0) -> float:
    return max_limit / (1 + math.exp(-rate * (time_step - offset)))


def start_and_wait_processes(subprocesses: list[Process]) -> None:
    for index, process in enumerate(subprocesses):
        process.start()
        time.sleep(get_sigmoid_sleep_seconds(index))

    exists_running_subprocess = True

    while exists_running_subprocess:
        exists_running_subprocess = False
        for process in subprocesses:
            exists_running_subprocess = process.is_alive() or exists_running_subprocess
        time.sleep(2)


def merge_sorted_batch_files(files: list, output_file_name: str, delete_originals=False) -> None:
    cur_queue = copy.deepcopy(files)
    counter = 0
    files_to_delete = files if delete_originals else []
    while len(cur_queue) > 0:
        cur_queue, new_queue = split_files(cur_queue)

        if len(cur_queue) == 1:
            shutil.move(cur_queue[0], output_file_name)
            break

        if len(cur_queue) == 2:
            file1, file2 = cur_queue
            merge_two_sorted_files(file1, file2, output_file_name)
            break

        subprocesses = []
        for index in range(0, len(cur_queue), 2):
            temp_file_name = f'temp_{output_file_name}_merge_{counter}.txt'
            new_queue.append(temp_file_name)
            files_to_delete.append(temp_file_name)
            p = Process(target=merge_two_sorted_files, args=(cur_queue[index], cur_queue[index + 1], temp_file_name))
            subprocesses.append(p)
            counter += 1

        start_and_wait_processes(subprocesses)

        cur_queue = new_queue
    delete_files(files_to_delete)
    return


def count_uniq_lines(inp: str, out: str) -> None:
    with open(inp, 'r') as inp_file, \
            open(out, 'w') as out_file:
        prev_line = inp_file.readline()
        cur_line = inp_file.readline()
        counter = 1
        while cur_line != '':
            if prev_line == cur_line:
                counter += 1
            else:
                out_file.write(f'{counter} {prev_line}')
                counter = 1
                prev_line = cur_line
            cur_line = inp_file.readline()
    return


def choose_random_ticket(current_ticket: str, new_tickets: list[str], prob_dist: list[float]) -> str:
    new_ticket = s.choice(new_tickets)
    return random.choices([current_ticket, new_ticket], weights=prob_dist)[0]


def determine_prob_dist(prev_total: int, num_new_ele: int) -> list[float]:
    new_total = prev_total + num_new_ele
    return [x / new_total for x in [prev_total, num_new_ele]]


def find_lotto_ticket(lotto_type: str, last_winning_ticket: str, next_lotto_date: str) -> (int, list):
    chosen_ticket = None
    file_name_prefix = f'{lotto_type}_{next_lotto_date}_find'
    file_counter = 0
    file_names = []
    index = 0
    while True:
        tickets = gen_batch_tickets(lotto_type)
        file_name = f'{file_name_prefix}_{file_counter}.txt'
        file_names.append(file_name)
        write_batch_to_file(file_name, tickets)
        if last_winning_ticket in tickets:
            index += tickets.index(last_winning_ticket)
            break
        index += len(tickets)
        file_counter += 1
    return index, file_names


def gen_lotto_ticket(lotto_type: str, count: int, next_lotto_date: str) -> list:
    file_name_prefix = f'{lotto_type}_{next_lotto_date}_play'
    file_counter = 0
    file_names = []
    while count > 0:
        tickets = gen_batch_tickets(lotto_type, min(c.BATCH_SIZE, count))
        file_name = f'{file_name_prefix}_{file_counter}.txt'
        file_names.append(file_name)
        write_batch_to_file(file_name, tickets)
        count -= c.BATCH_SIZE
        file_counter += 1
    return file_names
