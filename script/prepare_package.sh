#!/bin/bash

cd $(dirname "$0")
cd ..
cp script/start.* .
zip -19qr workPixil.zip source template src start.*
rm start.*
exit 0