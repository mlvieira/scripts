#!/bin/env sh

curl -s wttr.in/Canoas?1n | sed '1d' | head -n 6

sleep 30000 # huge workaround
