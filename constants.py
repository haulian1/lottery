import pytz

BATCH_SIZE = 2000000


class DateTime:
    TIME_ZONE = pytz.timezone("America/New_York")


class Modes:
    POWERBALL = 'POWER'
    MEGAMILLION = 'MEGA'


class Regex:
    MEGAMILLION = r"(0[1-9]|[1-6][0-9]|70){5}([0-1][1-9]|2[0-5])"
    POWERBALL = r"(0[1-9]|[1-6][0-9]){5}([0-1][1-9]|2[0-6])"


class Mega:
    WHITE_BALL_LIMIT = 70
    SPECIAL_BALL_LIMIT = 25
    DAY_OFFSETS = [(1, 1), (0, 3), (2, 2), (1, 1), (0, 4), (3, 3), (2, 2)]


class Power:
    WHITE_BALL_LIMIT = 69
    SPECIAL_BALL_LIMIT = 26
    DAY_OFFSETS = [(0, 2), (1, 1), (0, 3), (2, 2), (1, 1), (0, 2), (1, 1)]


class Error:
    EXIT_STATUS = {
        'get_days_offset': 1,
        'get_next_lotto_date': 2
    }
