#!/bin/bash

date_str=$(date +%m%d)
mkdir -p /srv/bak
mv /srv/empress.tar "/srv/bak/${date_str}.tar"

rm -rf /srv/empress
