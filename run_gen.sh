#!/bin/bash

## declare an array variable
declare -a arr=(84 65 131 0 23 187 99 153 44 112)

## now loop through the above array
for i in "${arr[@]}"
do
   #echo $i
   python3 genetic_modified.py $i 2>/home/crysys/project/logs/$i.err | tee /home/crysys/project/logs/$i.log &
   # or do whatever with individual element of the array
done
# You can access them using echo "${arr[0]}", "${arr[1]}" also