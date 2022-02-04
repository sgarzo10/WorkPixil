#!/bin/bash

cd $(dirname "$0")
zip -19qr workPixil.zip source template gui_manager.py work_pixil.py start.bat start.sh string.json
exit 0