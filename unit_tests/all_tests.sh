#!/usr/bin/env bash

for i in {0..5..2}
do 
    ./bridge_test.sh
done
for i in {0..5..2}
do
    ./random_data_test.sh
done
	 
