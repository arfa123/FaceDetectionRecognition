#!/bin/bash

source /home/pi/.profile
workon cv
sudo modprobe bcm2835-v4l2
python /home/pi/Desktop/Project/main2/main.py
