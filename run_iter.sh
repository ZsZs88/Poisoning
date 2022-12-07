#!/bin/bash

for i in $(seq 0 3)
do
   ./_run_iter.sh $i &
done