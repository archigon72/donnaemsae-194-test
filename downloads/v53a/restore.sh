#!/bin/sh
set -e
cat donnaemsae-194-test_v5.3a_16ecc2d.zip.part* > donnaemsae-194-test_v5.3a_16ecc2d.zip
sha256sum -c FULL_ZIP_SHA256.txt
python3 -m zipfile -t donnaemsae-194-test_v5.3a_16ecc2d.zip
python3 -m zipfile -e donnaemsae-194-test_v5.3a_16ecc2d.zip .
cd donnaemsae-194-test_v5.3a_16ecc2d && sha256sum --quiet -c ../FILES_SHA256.txt && echo "ALL $(wc -l < ../FILES_SHA256.txt) FILES OK"
