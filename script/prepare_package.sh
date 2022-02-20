#!/bin/bash

cd $(dirname "$0")
cd ..
cp script/start.* .
rm source/.DS_Store
rm -rf src/__pycache__
zip -19qr workPixil.zip source template src start.*
rm start.*
exit 0