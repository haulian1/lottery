# LOTTERY

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
