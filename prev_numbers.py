import os.path
from datetime import datetime
import json

import requests as r
import re

cur_year = datetime.now().year

dates = []
dates = [(f'01/01/{year}', f'12/31/{year}') for year in range(2010, cur_year+1)]
url = 'https://www.megamillions.com/cmspages/utilservice.asmx/GetDrawingPagingData'

raw_data = []

for start_date, end_date in dates:
    request_data = {"pageSize": 200, "startDate": start_date, "endDate": end_date, "pageNumber": 1}
    raw_data.append(
        json.loads(
            re.search(
                r'>{.*}<',
                r.post(url = url, data=request_data).text)[0][1:-1]))

lottery_numbers = []
occurrences = {}
from_file = []

print(f'hi')

file_name = 'past_winning_numbers.txt'

if not os.path.exists(file_name):
    with open(file_name, 'w') as file:
        for year in raw_data:
            for item in year:
                if item == 'DrawingData':
                    # print(len(data[item]))
                    for sub_item in year[item]:
                        # print(sub_item)
                        numbers = []
                        for ticket_data in sub_item:
                            if ticket_data[0] == 'N' or ticket_data == 'MBall':
                                number = sub_item[ticket_data]
                                numbers.append(number)
                                if number not in occurrences:
                                    occurrences[number] = 0
                                occurrences[number] += 1
                            # print(ticket_data)
                        file.write(','.join([str(x) for x in numbers]))
                        file.write('\n')
                        lottery_numbers.append(numbers)
else:
    print(f'green')
    with open(file_name, 'r') as file:
        cur_line = file.readline().strip()
        # print(cur_line)
        counter = 0
        while cur_line != '':
            print(f'cur line: {cur_line}')
            nums = []
            for x in cur_line.split(','):
                x = int(x)
                print(f'x: {x}')
                nums.append(x)
                if x not in occurrences:
                    occurrences[x] = 0
                occurrences[x] += 1
            lottery_numbers.append(nums)
            cur_line = file.readline().strip()

print('yellow')

for numbers in lottery_numbers:
    print(numbers)

for k,v in sorted(occurrences.items(), key=lambda x:x[0]):
    print(k, ": ", v)