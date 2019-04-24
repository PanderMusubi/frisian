#!/usr/bin/env sh

if [ ! -e ../download ]; then
	mkdir ../download
fi
cd ../download

if [ -e update.xml ]; then
	rm -f update.xml
fi
wget https://www.fryske-akademy.nl/spell/oxt/update.xml
if [ -e fy_NL-*.oxt ]; then
	rm -f fy_NL-*.oxt
fi
wget `grep xlink:href update.xml|awk -F '="' '{print $2}'|awk -F '"' '{print $1}'`

cd ../scripts
