#!/bin/sh
set -e
cat donnaemsae-194-test_v5.3_ed66d27.zip.part* > donnaemsae-194-test_v5.3_ed66d27.zip
sha256sum -c FULL_ZIP_SHA256.txt
python3 -m zipfile -t donnaemsae-194-test_v5.3_ed66d27.zip
python3 -m zipfile -e donnaemsae-194-test_v5.3_ed66d27.zip .
cd donnaemsae-194-test_v5.3_ed66d27 && sha256sum --quiet -c ../FILES_SHA256.txt && echo "ALL $(wc -l < ../FILES_SHA256.txt) FILES OK"
