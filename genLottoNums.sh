#!/bin/bash 

lottoKind=$1
pastWinLottoTicket=$2

echo "Lotto kind is: $lottoKind"
echo "Past winning lotto ticket is: $pastWinLottoTicket"
if [[ $lottoKind != 'MEGA' && $lottoKind != 'POWER' ]]; then
    echo "LOTTO KIND NOT 'MEGA' OR 'POWER' ERROR"
    echo "CHECK FIRST ARGUMENT TO SCRIPT"
    echo "EXITING SCRIPT"
    exit 1
fi

cd ~/projects/lottery

if [[ $lottoKind == 'MEGA' ]];then
    echo 'cd into MEGA'
    cd MEGA
else 
    echo 'cd into POWER'
    cd POWER
fi

baseDir=$(pwd)

###
#
#  `echo`s the next lotto day based on the kind of Lotto being played.
#  args: string - ddd, int - hh
#  echo: string - ddd
#
###
function getNextLottoDay {
    case $1 in
        'Mon' )
            if [[ $lottoKind == 'MEGA' ]]; then
                echo 'Tue'
                exit 0
            elif [[ $lottoKind == 'POWER' ]]; then
                if [[ $2 -lt 23 ]]; then
                    echo 'Mon'
                    exit 0
                else
                    echo 'Wed'
                    exit 0
                fi
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        'Tue' )
            if [[ $lottoKind == 'MEGA' ]]; then
                if [[ $2 -lt 23 ]]; then
                    echo 'Tue'
                    exit 0
                else
                    echo 'Fri'
                    exit 0
                fi
            elif [[ $lottoKind == 'POWER' ]]; then
                echo 'Wed'
                exit 0
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        'Wed' )
            if [[ $lottoKind == 'MEGA' ]]; then
                echo 'Fri'
                exit 0
            elif [[ $lottoKind == 'POWER' ]]; then
                if [[ $2 -lt 23 ]]; then
                    echo 'Wed'
                    exit 0
                else
                    echo 'Sat'
                    exit 0
                fi
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        'Thu' )
            if [[ $lottoKind == 'MEGA' ]]; then
                echo 'Fri'
                exit 0
            elif [[ $lottoKind == 'POWER' ]]; then
                echo 'Sat'
                exit 0
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        'Fri' )
            if [[ $lottoKind == 'MEGA' ]]; then
                if [[ $2 -lt 23 ]]; then
                    echo 'Fri'
                    exit 0
                else
                    echo 'Tue'
                    exit 0
                fi
            elif [[ $lottoKind == 'POWER' ]]; then
                echo 'Sat'
                exit 0
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        'Sat' )
            if [[ $lottoKind == 'MEGA' ]]; then
                echo 'Tue'
                exit 0
            elif [[ $lottoKind == 'POWER' ]]; then
                if [[ $2 -lt 23 ]]; then
                    echo 'Sat'
                    exit 0
                else
                    echo 'Mon'
                    exit 0
                fi
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        'Sun' )
            if [[ $lottoKind == 'MEGA' ]]; then
                echo 'Tue'
                exit 0
            elif [[ $lottoKind == 'POWER' ]]; then
                echo 'Mon'
                exit 0
            else
                echo 'ERROR'
                exit 1
            fi
            ;;
        * )
            echo 'NO MATCH ERROR'
            exit 1
            ;;
    esac
}

###
#
#  `echo`s the next lotto date based on the kind of Lotto being played.
#  echo: string (mm_dd_yyyy)
#
###
function getNextLottoDate {
    dayOfWeek=$(date '+%a')
    hourOfDay=$(date '+%H')

    nextLottoDayOfWeek=$(getNextLottoDay $dayOfWeek $hourOfDay)
    echo $(date -d $nextLottoDayOfWeek '+%m_%d_%Y')
    exit 0
}



lottoDate=$(getNextLottoDate $lottoKind)

lottoFindFileName=$lottoDate"_find.txt"
lottoPlayFileName=$lottoDate"_play.txt"

splitFindFolderName=$lottoDate"_find_split"
splitPlayFolderName=$lottoDate"_play_split"

echo "
Lotto date is: $lottoDate
lottoFindFileName is: $lottoFindFileName 
lottoPlayFileName is: $lottoPlayFileName 
splitFindFolderName is: $splitFindFolderName
splitPlayFolderName is: $splitPlayFolderName
"
echo "
FINDING LAST WINNING LOTTO TICKET
"
python3 ../gen_lotto_nums.py $lottoKind 'FIND' $pastWinLottoTicket > $lottoFindFileName

exitStatus=$?
if [[ $exitStatus -ne 0 ]]; then
    echo "FINDING LOTTO NUMBER ERROR"
    echo "EXIT STATUS: $exitStatus"
    echo "EXITING SCRIPT"
    exit 1
fi

echo "
Finished finding past winning lotto number
"


iter=$(grep -in $pastWinLottoTicket $lottoFindFileName | sed 's/\(.*\):.*/\1/g')

echo "
The iteration the past winning was found on was: $iter
"

python3 ../gen_lotto_nums.py $lottoKind 'CHOOSE' $iter > $lottoPlayFileName &

playPID=$!
echo "
Play with iteration has been sent to background process with processID: $!
"

mkdir $splitFindFolderName
cd $splitFindFolderName

echo "
Current directory is: $(pwd)
"

echo "
Spliting files for $lottoFindFileName
"
split -l 10000000 ../$lottoFindFileName
echo "
Splitting done
"
echo "
Sorting and finding uniq counts
===============================
"
ls | while read file; 
do
    echo "Processing file $file"
    sort $file | uniq -c | sort -r > uniq_sorted_$file
    echo "Done"

done


echo "
===============================
Sorting and finding uniq counts done
"

echo "
Combining the uniq sorted file and removing lotto tickets that show up less than 4 times
"
grep -vi '1 \|2 \|3 ' uniq* | awk '{print $2 " " $3}' | sort -k 2 > combined_uniq_sorted

echo "
Finding any number that is more than 4 times across multiple files
"
awk '{print $2}' combined_uniq_sorted | sort | uniq -c | grep -vi '1 ' > multiple_hits_across_files

echo "
Finished processing FIND
"
echo 

echo "
Going to baseDir $baseDir
"
cd $baseDir

mkdir $splitPlayFolderName
cd $splitPlayFolderName

echo "
Switching to play directory $splitPlayFolderName
Current directory is: $(pwd)
"
counter=0

echo "
Checking that the $lottoPlayFileName has been created
"
while [[ $counter -le 3 ]];do
    if [[ -f ../$lottoPlayFileName ]]; then
        break
    else
        sleep 15
    fi
    counter=$((counter++))
done

curNumLines=$(wc -l ../$lottoPlayFileName | awk '{print $1}')
if [[ $counter -eq 3 && \
      ! -f ../$lottoPlayFileName && \
      $curNumLines -gt 0 ]]; then
    echo
    echo "THERE WAS AN ERROR GENERATING THE PLAY FILE."
    echo "FILE $lottoPlayFileName DNE"
    echo "EXITING SCRIPT"
    echo
    exit 1
fi
echo "
Done. File exists AND is not empty.
"

echo "
Checking that adding lotto numbers are done
"

iter=$(grep -in $pastWinLottoTicket $lottoFindFileName | sed 's/\(.*\):.*/\1/g')
while [[ $curNumLines -lt $iter ]]; do
    sleep 20
    curNumLines=$(wc -l ../$lottoPlayFileName | awk '{print $1}')
    echo "curNumLines: $curNumLines"
    echo "$(($iter-$curNumLines)) more tickets to go"
    echo 
done

echo "
Done adding lotto numbers.
"

echo "
Spliting files
"
split -l 10000000 ../$lottoPlayFileName
echo "
Spliting Done
"

echo "
Sorting and finding uniq counts
===============================
"
ls | while read file; do
    echo "Processing file $file"
    sort $file | uniq -c | sort -r > uniq_sorted_$file
    echo "Done"
done
echo "
===============================
Sorting and finding uniq counts done
"

echo "Combining the uniq sorted file and removing lotto tickets that show up less than 4 times"
grep -vi '1 \|2 \|3 ' uniq* | awk '{print $2 " " $3}' | sort -k 2 > combined_uniq_sorted

echo "Finding any number that is more than 4 times across multiple files"
awk '{print $2}' combined_uniq_sorted | sort | uniq -c | grep -vi '1 ' > multiple_hits_across_files

echo "Finished processing PLAY"

echo "
ALL DONE
:)
"

