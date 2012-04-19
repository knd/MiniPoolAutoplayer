#!/bin/bash

xdotool search --class google-chrome windowactivate
xdotool mousemove 1433 153

for i in {1..100}
do
    xdotool click 1
	sleep 0.05
done
xdotool mousemove 1433 869
for i in {1..10}
do
  xdotool click 1
  sleep 0.05
done
sleep 2
xdotool mousemove 629 552 click 1
sleep 3
