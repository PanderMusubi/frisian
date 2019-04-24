#!/usr/bin/env sh

if [ ! -e ../download ]; then
	echo 'ERROR: Missing download directory'
	exit 1
fi
cd ../download

if [ ! -e fy_NL-*.oxt ]; then
	echo 'ERROR: Missing file fy_NL-*.oxt'
	exit 1
fi
if [ -e extracted ]; then
	rm -rf extracted
fi
mkdir extracted
cd extracted
unzip -q ../fy_NL-*.oxt
cd ..

cd ../scripts
