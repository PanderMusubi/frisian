from datetime import datetime
from locale import LC_ALL, setlocale, strxfrm
from operator import itemgetter
from os.path import isfile
from os import rename, remove

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
	print(name)
	values = ''
	for value, count in sorted(data.items(), key=itemgetter(1), reverse=True):
		print('{}\t{}'.format(count, value))
		values += value
	print('{}'.format(values))
	ret = values
	values = ''
	for value in sorted(data, key=strxfrm):
		values += value
	print('{}'.format(values))
	return ret

if not isfile('../generated/fy_NL.aff'):
	print('ERROR: Missing file ../generated/fy_NL.aff')
	exit(1)
if not isfile('../generated/fy_NL.dic'):
	print('ERROR: Missing file ../generated/fy_NL.dic')
	exit(1)

try:
	setlocale(LC_ALL, 'nl_NL.UTF-8')
except:
	try:
		setlocale(LC_ALL, 'en_US.UTF-8')
	except:
		print('ERROR: Could not set sorting')
		exit(1)

now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
option_keepcase = ''
option_try = ''
corrections = {}
version = None
#chars_aff = {}
for line in open('../generated/fy_NL.aff'):
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

errors = open('../test/fy_NL.tsv', 'w')
for error, values in sorted(corrections.items()):
	errors.write('{}\t{}\n'.format(error, sorted(values)[0])) #TODO
tests = open('../test/test_incorrect_words_with_suggestion.txt', 'w')
for test, values in sorted(corrections.items()):
	tests.write('{}\n'.format(test))

#chars_dic = {}
first = True
words = set()
nr_words = 0
nr_flags = 0
exclude_words = set()
for line in open('../generated/fy_NL.dic'):
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
		print('WARNING: Duplicate word {} from {}'.format(line, org))
	else:
		words.add(line)
		nr_words += 1
	if flags:
		if flags == 'P':
			nr_flags += 1
			if line[0] == 'â':
				prefixed = 'A' + line[1:]
				if prefixed in words:
					print('WARNING: Excluding duplicate prefixed word {} from {}'.format(prefixed, org))
					exclude_words.add(prefixed)
				else:
					words.add(prefixed)
			elif line[0] == 'ô':
				prefixed = 'O' + line[1:]
				if prefixed in words:
					print('WARNING: Excluding duplicate prefixed word {} from {}'.format(prefixed, org))
					exclude_words.add(prefixed)
				else:
					words.add(prefixed)
			elif line[0] == 'ú' or line[0] == 'û':
				prefixed = 'UA' + line[1:]
				if prefixed in words:
					print('WARNING: Excluding duplicate prefixed word {} from {}'.format(prefixed, org))
					exclude_words.add(prefixed)
				else:
					words.add(prefixed)
			else:
				print('ERROR: Flag mismatch {} from org'.format(line, org))
				exit(1)
		else:
			print('ERROR: Unsupported flags {} from {}'.format(flags, org))
			exit(1)
#order_dic = histogram(chars_dic, 'chars_dic')

# Writing word list
wordlist = open('../generated/frisian', 'w')
histogram = {}
for word in sorted(words, key=strxfrm):
	for char in word:
		if char in histogram:
			histogram[char] += 1
		else:
			histogram[char] = 1
	wordlist.write('{}\n'.format(word))
#print('INFO: Read {} words'.format(nr_words))
#print('INFO: Found {} flags'.format(nr_flags))
#print('INFO: Wrote {} words'.format(len(words)))
#print('INFO: Total {}'.format(nr_words+nr_flags))

sorted_values = ''
missing = set()
for value, count in sorted(histogram.items(), key=itemgetter(1), reverse=True):
	sorted_values += value
for value in alphabet:
	if value not in sorted_values:
		missing.add(value)

print('INFO: Value for TRY {}'.format(option_try))
print('INFO: Improved  TRY {}'.format(sorted_values))
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
print('INFO: Extra characters in new TRY {}'.format(extra))
print('INFO: Missing characters from alphabet in new TRY {}'.format(''.join(missing)))
removed = ''
for char in missing:
	if char in option_try:
		removed += char
if removed != '':
	print('WARNING: Characters removed from original TRY {}'.format(removed))
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
tmp = open('../generated/fy_NL.aff.tmp', 'w')
tmp.write('# Improved version by https://github.com/PanderMusubi/frisian from {}\n'.format(now))
for line in open('../generated/fy_NL.aff'):
	if line.startswith('TRY'):
		# set encoding to UTF-8
		print('INFO: Adding SET')
		tmp.write('SET UTF-8\n')
		# support QEWRTY and AZERTY keyboards
		print('INFO: Adding KEY')
		tmp.write('KEY qwertyuiop|asdfghjkl|zxcvbnm|qawsedrftgyhujikolp|azsxdcfvgbhnjmk|aze|qsd|lm|wx|aqz|qws\n')
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
		tmp.write('TRY {}\n'.format(sorted_values))
	else:
		tmp.write(line)
remove('../generated/fy_NL.aff')
rename('../generated/fy_NL.aff.tmp', '../generated/fy_NL.aff')

# Improvind dic file
tmp = open('../generated/fy_NL.dic.tmp', 'w')
first = True
for line in open('../generated/fy_NL.dic'):
	if first:
		tmp.write('{} '.format(nr_words - len(exclude_words)))
		tmp.write(line.strip()[line.index('Copyright'):])
		tmp.write(' Improved version by https://github.com/PanderMusubi/frisian from {}\n'.format(now))
		first = False
		continue
	stripped = line.strip()
	if stripped in exclude_words:
		continue
	tmp.write(line)
remove('../generated/fy_NL.dic')
rename('../generated/fy_NL.dic.tmp', '../generated/fy_NL.dic')
