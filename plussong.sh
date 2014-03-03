#!/bin/bash

./status.sh | while :
do
        read line
        playing=$(ncmpcpp --now-playing)
        echo "$playing | $line" || exit 1
done
