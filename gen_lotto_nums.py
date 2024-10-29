import secrets as s
import sys
import re as regex

class modes:
    POWERBALL_MODE = 'POWER'
    MEGAMILLION_MODE = 'MEGA'
    
class runs:
    FIND = 'FIND'
    CHOOSE = 'CHOOSE'

BATCH_SIZE = 2000000

WHITE_POWER_BALL_LIMIT = 69
POWER_BALL_LIMIT = 26

WHITE_MEGA_BALL_LIMIT = 70
MEGA_BALL_LIMIT = 25

def gen_ball(limit):
    return s.randbelow(limit) + 1

def get_white_balls(mode):
    max_num_white = None
    match mode:
        case modes.POWERBALL_MODE:
            max_num_white = WHITE_POWER_BALL_LIMIT
        case modes.MEGAMILLION_MODE:
            max_num_white = WHITE_MEGA_BALL_LIMIT
        case _:
            pass

    nums = set([])
    while len(nums) < 5:
        num = gen_ball(max_num_white)
        nums.add(num)
    return ''.join([str(x) if x >= 10 else '0' + str(x) for x in sorted(nums)])

def gen_special_ball(mode):
    max_num_special = None
    match mode:
        case modes.POWERBALL_MODE:
            max_num_special = POWER_BALL_LIMIT
        case modes.MEGAMILLION_MODE:
            max_num_special = MEGA_BALL_LIMIT
        case _:
            pass
    special = gen_ball(max_num_special)
    return str(special) if special >= 10 else '0' + str(special)

def gen_ticket(mode):
    nums = get_white_balls(mode) + gen_special_ball(mode)
    return nums

def generate_mult_tickets(num_tics, mode):
    gen_tickets = []
    for i in range(num_tics):
        gen_tickets.append(gen_ticket(mode))
    return gen_tickets

def find_winning_ticket(winning_ticket, mode):
    found_winning_ticket = False

    while not found_winning_ticket:
        tickets = generate_mult_tickets(BATCH_SIZE, mode)
        print("\n".join(tickets))
        if winning_ticket in tickets:
            found_winning_ticket = True

def choose_ticket(num_tics, mode):
    for i in range(num_tics, 0, -BATCH_SIZE):
        tickets = generate_mult_tickets(BATCH_SIZE if i > BATCH_SIZE else i, mode)
        print("\n".join(tickets))
        num_tics -= BATCH_SIZE


def run(mode, run, winning_ticket, winning_ticket_position):
    if mode == modes.POWERBALL_MODE:
        if run == runs.FIND:
            find_winning_ticket(winning_ticket, modes.POWERBALL_MODE)
        else:
            choose_ticket(winning_ticket_position, modes.POWERBALL_MODE)
    else:
        if run == runs.FIND:
            find_winning_ticket(winning_ticket, modes.MEGAMILLION_MODE)
        else:
            choose_ticket(winning_ticket_position, modes.MEGAMILLION_MODE)

def find(ticket, mode):
    return run(mode, runs.FIND, ticket, None)

def choose(iteration, mode):
    return run(mode, runs.CHOOSE, None, iteration)

def find_mega(ticket):
    return find(ticket, modes.MEGAMILLION_MODE)

def choose_mega(iteration):
    return choose(iteration, modes.MEGAMILLION_MODE)

def find_powerball(ticket):
    return find(ticket, modes.POWERBALL_MODE)

def choose_powerball(iteration):
    return choose(iteration, modes.POWERBALL_MODE)

def verify_args(mode, run, arg):
    match mode.upper():
        case modes.MEGAMILLION_MODE:
            match run.upper():
                case runs.FIND:
                    if len(arg) != 12:
                        sys.exit(2)
                    return bool(regex.match(r"([0][1-9]|[1-6][0-9]|70){5}([0-1][1-9]|[2][0-5])", arg)) 
                case runs.CHOOSE:
                    arg = int(arg)
                    return arg > 0 
        case modes.POWERBALL_MODE:
            match run.upper():
                case runs.FIND:
                    if len(arg) != 12:
                        sys.exit(3)
                    return bool(regex.match(r"([0][1-9]|[1-6][0-9]){5}([0-1][1-9]|[2][0-5])", arg)) 
                case runs.CHOOSE:
                    arg = int(arg)
                    return arg > 0 
    sys.exit(4)

mode_type = sys.argv[1]
run_type = sys.argv[2]
arg = sys.argv[3]

if verify_args(mode_type, run_type, arg):
    if mode_type == modes.MEGAMILLION_MODE:
        if run_type == runs.FIND:
            find_mega(arg)
        else:
            arg = int(arg)
            choose_mega(arg)
    else:
        if run_type == runs.FIND:
            find_powerball(arg)
        else:
            arg = int(arg)
            choose_powerball(arg)
else:
    sys.exit(5)
