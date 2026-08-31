#!/bin/bash

if [ -f /srv/run/empress.pid ]; then
    kill $(cat /srv/run/empress.pid)
else
    echo "the PID file /srv/run/empress.pid does not exist"
fi
