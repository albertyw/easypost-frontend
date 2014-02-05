#!/bin/bash

# a simple script to run the server

python src/serve.py -p 9001
sleep 2s
/bin/bash scripts/runserver.sh "$@"
