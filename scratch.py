import sys

import helpers as h

try:
    lotto_type, last_winning_ticket = sys.argv
except:
    sys.exit(h.get_exit_status('invalid_args'))

lotto_type = h.validate_lotto_type(lotto_type)
h.validate_lotto_ticket(last_winning_ticket)

next_lotto_date = h.get_next_lotto_date(lotto_type)

found_iteration, find_files = h.find_lotto_ticket(lotto_type, last_winning_ticket, next_lotto_date)
combined_find_file_name = f'find_{next_lotto_date}_combined.txt'
uniq_combined_find_file_name = f'uniq_{combined_find_file_name}'
h.merge_sorted_batch_files(find_files, combined_find_file_name)
h.count_uniq_lines(combined_find_file_name, uniq_combined_find_file_name)

play_files = h.gen_lotto_ticket(lotto_type, found_iteration, next_lotto_date)
combined_play_file_name = f'play_{next_lotto_date}_combined.txt'
uniq_combined_play_file_name = f'uniq_{combined_play_file_name}'
h.merge_sorted_batch_files(play_files, combined_play_file_name)
h.count_uniq_lines(combined_play_file_name, uniq_combined_play_file_name)


