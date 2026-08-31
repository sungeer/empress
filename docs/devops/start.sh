#!/bin/bash

nohup /srv/venvs/empress/bin/python /srv/empress/main.py > /dev/null 2>&1 &
echo $! > /srv/run/empress.pid
