#!/bin/bash

cd $(dirname "$0")
python3 gui_manager.py 1>/dev/null 2>/dev/null &
exit 0
