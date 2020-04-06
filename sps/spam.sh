#!/bin/bash

for i in {1..10}
do
	sudo python3 main.py MCST-2-$i > /dev/null &
done
