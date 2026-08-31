#!/bin/bash

if [ -f /srv/run/empress.pid ]; then
    pid=$(cat /srv/run/empress.pid)
    if kill -0 "$pid" 2>/dev/null; then
        echo "empress is running, pid=$pid"
        tail -20 /srv/logs/empress.log
    else
        echo "empress is NOT running (stale pid=$pid)"
        exit 1
    fi
else
    echo "the PID file /srv/run/empress.pid does not exist"
    exit 1
fi
