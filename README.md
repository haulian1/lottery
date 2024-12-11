# LOTTERY

## Story

Have you ever thought to yourself,\
"what if I had my own lotto number generator?" well fear no more. \
This project can help you achieve that.  \
All you need is Python 3.10 or later (... and lots? of disk space ... see caveats)

Instead of just using the random library, I wanted to try the secrets library that was [cryptographically secure](https://docs.python.org/3/library/secrets.html).\
Do I need cryptographically secure randomness? No\
Will I use it though? HECK YEAH!

## Usage
1. Run the script in the terminal by doing `python3 gen_lotto_numbers.py ['MEGA' | 'POWER'] '<LastWinningLottoTicket>'`
   1. E.G. Given the winning ticket on 2024/11/29 of 3, 29, 34, 37, 38 + 17
   2. The command to run would be 
   3. `$ python3 gen_lotto_numbers.py 'MEGA' '032934373817'`
2. The script will generate numbers at the specified `BATCH_SIZE` in `constants.py`
3. Each batch will be a file on its own with a counter
4. The script will keep generating random tickets until the batch where the last winning ticket was generated
   1. The files generated while finding the last wining tickets will be merged into a single file.  
   2. During this time there may be many temporary files created to hold the intermediate merges.
   3. The temporary files will be deleted when the merging is completed.
   4. The merged file is in sorted order.
   5. The file will have the word `find` in the name with the date for the next drawing
   6. Once the merged file has been created, a file with the unique count of the numbers will be generated.
      1. The file will have lines such as `10 022145525308`
      2. This means that the ticket `022145525308` was generated 10 times during script execution
5. Once the ticket is found, `n`-number of new tickets will be generated 
   1. `n` is the iteration where the last winning ticket was found
6. Once all `n` tickets have been generated, the same merge process will take place as described in part 4.
7. The script is will move all the files generated during the run into a folder
   1. For the example command in 1.c given the conditions of 1
   2. The folder will be named `MEGA_2024_12_3`
   3. There will be 4 files in the folder:
      1. `find_2024_12_3_combined.txt`
      2. `play_2024_12_3_combined.txt`
      3. `uniq_find_2024_12_3_combined.txt`
      4. `uniq_play_2024_12_3_combined.txt`
8. The script has now finished

## Choosing a ticket

I normally use some bash commands to help me choose a ticket. \
You can use whatever way you like to choose a ticket by choosing the line you want from one of the 4 files.

Here is what I normally run in order to get the ticket(s) I want to play
```bash
cd name_of_folder
ls | while read file;
do
    lines=$(( $(wc -l $file | awk '{print $1}') + 1 ))
    choice=$(python3 -S -c "import secrets as s; print(s.randbelow($lines)+1);")
    sed "$choiceq;d" $file
done
```

## Caveats

1. I have noticed that sometimes it takes very very VERY long to get to generating the last winning ticket. 
In these cases, there are a lot of files that are generated and there is also a lot of space that it ends up taking up.  
So, I would recommend that you keep an eye on your disk space if you are generating these lotto tickets.

## Improvements

1. Parallelization
2. Memory usage enhancements