# lottery

## Usage
1. Requires that there is a folder called `MEGA` and `POWER` if trying to generate a lotto ticket for MegaMillions or PowerBall respectively.
1. Run the bash script with the arguments `MEGA` or `POWER` as the first argument and the last winning lotto numbers as the second argument
  1. Ex. `./genLottoNums.sh 'MEGA' '232635414307'
  1. NOTE: ALL numbers need to be 2-digits. Pad with '0' where necessary
1. There will be files created in the respective `MEGA` or `POWER` folders with the date on which the drawing will happen.

## Caveats
1. The `date` command uses `GNU`'s `date` 
