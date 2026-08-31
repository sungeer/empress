#!/bin/bash

result=$(ps -ef | grep main.py | grep -v grep | grep -v '\.sh')
if [ -z "$result" ]; then
  echo "no empress"
else
  echo "empress list: "
  echo "$result"
fi
