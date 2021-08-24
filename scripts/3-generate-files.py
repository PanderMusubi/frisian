#!/usr/bin/env python3
'''Generate files.'''

from datetime import datetime
from locale import LC_ALL, setlocale, strxfrm
from operator import itemgetter
from os.path import isfile
from os import rename, remove
import sys

alphabet = ("'", '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'á', 'à', 'â', 'ä', 'å',
            'Á', 'À', 'Â', 'Ä', 'Å',
            'é', 'è', 'ê', 'ë',
            'É', 'È', 'Ê', 'Ë',
            'í', 'ì', 'î', 'ï',
            'Í', 'Ì', 'Î', 'Ï',
            'ó', 'ò', 'ô', 'ö',
            'Ó', 'Ò', 'Ô', 'Ö',
            'ú', 'ù', 'û', 'ü',
            'Ú', 'Ù', 'Û', 'Ü')

def histogram(data, name):
    ''' Return history.'''
    print(name)
    values = ''
    for value, count in sorted(data.items(), key=itemgetter(1), reverse=True):
        print(f'{count}\t{value}')
        values += value
    print(f'{values}')
    ret = values
    values = ''
    for value in sorted(data, key=strxfrm):
        values += value
    print(f'{values}')
    return ret

if not isfile('../generated/fy_NL.aff'):
    print('ERROR: Missing file ../generated/fy_NL.aff')
    sys.exit(1)
if not isfile('../generated/fy_NL.dic'):
    print('ERROR: Missing file ../generated/fy_NL.dic')
    sys.exit(1)

try:
    setlocale(LC_ALL, 'nl_NL.UTF-8')
except:  # pylint:disable=bare-except
    try:
        setlocale(LC_ALL, 'en_US.UTF-8')
    except:  # pylint:disable=bare-except
        print('ERROR: Could not set sorting')
        sys.exit(1)

now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
option_keepcase = ''
option_try = ''
corrections = {}
version = None
#chars_aff = {}
for line in open('../generated/fy_NL.aff'):  # pylint:disable=consider-using-with
    line = line.strip()
    # version
    if not version and 'copyright' in line.lower() and 'version: ' in line.lower():
        version = line.lower().split('version: ')[1].split()[0]
        continue
    # header or empty
    if line == '' or line[0] == '#':
        continue
    # histogram
#	for char in line:
#		if char in chars_aff:
#			chars_aff[char] += 1
#		else:
#			chars_aff[char] = 1
    # TRY
    if line.startswith('TRY'):
        option_try = line.split()[1]
        continue
    # KEEPCASE
    if line.startswith('KEEPCASE'):
        option_keepcase = line.split()[1]
        continue
    # REP
    if line.startswith('REP') and len(line.split()) == 3:
        option, error, word = line.split()
        if error[0] != '^' or error[-1] != '$':
            continue
        error = error[1:-1]
        if error not in corrections:
            corrections[error] = set()
        corrections[error].add(word)
        continue
#order_aff = histogram(chars_aff, 'chars_aff')

errors = open('../test/fy_NL.tsv', 'w')  # pylint:disable=consider-using-with
for error, values in sorted(corrections.items()):
    errors.write(f'{error}\t{sorted(values)[0]}\n') #TODO
tests = open('../test/test_incorrect_words_with_suggestion.txt', 'w')  # pylint:disable=consider-using-with
for test, values in sorted(corrections.items()):
    tests.write(f'{test}\n')

#chars_dic = {}
first = True
words = set()
nr_words = 0
nr_flags = 0
exclude_words = set()
for line in open('../generated/fy_NL.dic'):  # pylint:disable=consider-using-with
    if first:
        first = False
        continue
    line = line.strip()
    org = line
    flags = None
    if '/' in line:
        index = line.index('/')
        if line[index-1] != '\\':
            flags = line[index+1:]
            line = line[:index]
            if option_keepcase != '' and option_keepcase in flags:
                flags = flags.replace(option_keepcase, '')
#	for char in line:
#		if char in chars_dic:
#			chars_dic[char] += 1
#		else:
#			chars_dic[char] = 1
    if line in words:
        print(f'WARNING: Duplicate word {line} from {org}')
    else:
        words.add(line)
        nr_words += 1
    if flags:
        if flags == 'P':
            nr_flags += 1
            if line[0] == 'â':
                prefixed = 'A' + line[1:]
                if prefixed in words:
                    print(f'WARNING: Excluding duplicate prefixed word {prefixed} from {org}')
                    exclude_words.add(prefixed)
                else:
                    words.add(prefixed)
            elif line[0] == 'ô':
                prefixed = 'O' + line[1:]
                if prefixed in words:
                    print(f'WARNING: Excluding duplicate prefixed word {prefixed} from {org}')
                    exclude_words.add(prefixed)
                else:
                    words.add(prefixed)
            elif line[0] == 'ú' or line[0] == 'û':
                prefixed = 'UA' + line[1:]
                if prefixed in words:
                    print(f'WARNING: Excluding duplicate prefixed word {prefixed} from {org}')
                    exclude_words.add(prefixed)
                else:
                    words.add(prefixed)
            else:
                print(f'ERROR: Flag mismatch {line} from {org}')
                sys.exit(1)
        else:
            print(f'ERROR: Unsupported flags {flags} from {org}')
            sys.exit(1)
#order_dic = histogram(chars_dic, 'chars_dic')

# Writing word list
wordlist = open('../generated/frisian', 'w')  # pylint:disable=consider-using-with
histogram = {}
for word in sorted(words, key=strxfrm):
    for char in word:
        if char in histogram:
            histogram[char] += 1
        else:
            histogram[char] = 1
    wordlist.write(f'{word}\n')
#print(f'INFO: Read {nr_words} words')
#print(f'INFO: Found {nr_flags} flags')
#print(f'INFO: Wrote {len(words)} words')
#print(f'INFO: Total {nr_words+nr_flags}')

sorted_values = ''
missing = set()
for value, count in sorted(histogram.items(), key=itemgetter(1), reverse=True):
    sorted_values += value
for value in alphabet:
    if value not in sorted_values:
        missing.add(value)

print(f'INFO: Value for TRY {option_try}')
print(f'INFO: Improved  TRY {sorted_values}')
incl = ''
excl = ''
extra = ''
for char in sorted_values:
    if char in option_try:
        incl += char
        excl += ' '
    else:
        incl += ' '
        excl += char
        extra += char
#print(incl)
#print(excl)
print(f'INFO: Extra characters in new TRY {extra}')
print(f"INFO: Missing characters from alphabet in new TRY {''.join(missing)}")
removed = ''
for char in missing:
    if char in option_try:
        removed += char
if removed != '':
    print(f'WARNING: Characters removed from original TRY {removed}')
#incl = ''
#excl = ''
#for char in order_aff:
#	if char in option_try:
#		incl += char
#		excl += ' '
#	else:
#		incl += ' '
#		excl += char
#print(incl)
#print(excl)

# Improving aff file
tmp = open('../generated/fy_NL.aff.tmp', 'w')  # pylint:disable=consider-using-with
tmp.write(f'# Improved version by https://github.com/PanderMusubi/frisian from {now}\n')
for line in open('../generated/fy_NL.aff'):  # pylint:disable=consider-using-with
    if line.startswith('TRY'):
        # set encoding to UTF-8
        print('INFO: Adding SET')
        tmp.write('SET UTF-8\n')
        # support QEWRTY and AZERTY keyboards
        print('INFO: Adding KEY')
        tmp.write('KEY qwertyuiop|asdfghjkl|zxcvbnm|qawsedrftgyhujikolp'
                  '|azsxdcfvgbhnjmk|aze|qsd|lm|wx|aqz|qws\n')
        # support Unicode apostrophe and emphasis on double vowels
        print('INFO: Adding ICONV')
        tmp.write('ICONV 13\n')
        tmp.write('ICONV áá aa\n')
        tmp.write('ICONV áú au\n')
        tmp.write('ICONV éá ea\n')
        tmp.write('ICONV éé ee\n')
        tmp.write('ICONV éí ei\n')
        tmp.write('ICONV éú eu\n')
        tmp.write('ICONV íé ie\n')
        tmp.write('ICONV óé oe\n')
        tmp.write('ICONV óó oo\n')
        tmp.write('ICONV óú ou\n')
        tmp.write('ICONV úí ui\n')
        tmp.write('ICONV úú uu\n')
        tmp.write('ICONV ’ \'\n')
        # improve TRY
        print('INFO: Improving TRY')
        tmp.write(f'TRY {sorted_values}\n')
    else:
        tmp.write(line)
remove('../generated/fy_NL.aff')
rename('../generated/fy_NL.aff.tmp', '../generated/fy_NL.aff')

# Improvind dic file
tmp = open('../generated/fy_NL.dic.tmp', 'w')  # pylint:disable=consider-using-with
first = True
for line in open('../generated/fy_NL.dic'):  # pylint:disable=consider-using-with
    if first:
        tmp.write(f'{nr_words-len(exclude_words)} ')
        tmp.write(line.strip()[line.index('Copyright'):])
        tmp.write(f' Improved version by https://github.com/PanderMusubi/frisian from {now}\n')
        first = False
        continue
    stripped = line.strip()
    if stripped in exclude_words:
        continue
    tmp.write(line)
remove('../generated/fy_NL.dic')
rename('../generated/fy_NL.dic.tmp', '../generated/fy_NL.dic')
