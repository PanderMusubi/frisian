#!/usr/bin/env sh

if [ ! -e ../generated ]; then
	echo 'ERROR: Missing generated directory'
	exit 1
fi
cd ../generated

if [ ! -e ../test ]; then
	mkdir ../test
fi

if [ ! -e fy_NL.aff -a fy_NL.dic -a ! ../test/test_words.txt ]; then
	echo 'ERROR: Missing files fy_NL.aff, fy_NL.dic or test_words.txt'
	exit 1
fi

echo 'INFO: Testing '`wc -l frisian | awk '{print $1}'`' words from ../generated/frisian'
hunspell -d fy_NL -a frisian | grep '^#' > ../test/words_incorrect.txt
echo 'INFO: '`wc -l ../test/words_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/words_incorrect.txt'

echo 'INFO: Testing '`wc -l ../test/test_words.txt | awk '{print $1}'`' words from ../test/test_words.txt'
hunspell -d fy_NL -a ../test/test_words.txt | grep '^#' > ../test/tests_incorrect.txt
echo 'INFO: '`wc -l ../test/tests_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/tests_incorrect.txt'

cd ../scripts
