#!/bin/bash

for (( i=0+$1*50; i<=49+$1*50; i++ ))
do
   python3 poisoner_modified.py $i 2>/home/thesis/project/logs/$i.err
done