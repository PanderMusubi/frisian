#!/usr/bin/env sh

if [ ! -e ../download ]; then
	echo 'ERROR: Missing download directory'
	exit 1
fi
cd ../download

if [ ! -e extracted ]; then
	echo 'ERROR: Missing extracted directory'
	exit 1
fi

if [ ! -e ../generated ]; then
	mkdir ../generated
fi
if [ ! -e ../test ]; then
	mkdir ../test
fi
iconv -f ISO-8859-1 -t UTF-8//IGNORE extracted/fy_NL.dic -o ../generated/fy_NL.dic
iconv -f ISO-8859-1 -t UTF-8//IGNORE extracted/fy_NL.aff -o ../generated/fy_NL.aff

python3 ../scripts/3-generate-files.py

cd ../scripts
