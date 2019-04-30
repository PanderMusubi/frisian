# Frisian

![Frisian logo](images/logo.png?raw=true)

Word list and spell checking for Frisian (fy), a West Germanic language spoken
mostly in the province of Friesland (*Fryslân*) in the north of the Netherlands.
Note that with Frisian here, West Frisian is implied.


## Source

The source for the word list and spell checking, with permission and under the
same license, is the [Fryske Akademy](https://fryske-akademy.nl).


## Installation

Install the word list and spell checker packages from the `packages` directory
with the command `sudo dpkg -i` followed by the filenames of the packages that
need to be installed.

Command-line spell checkers such as Hunspell and Nuspell as well as GUI
applications such as LibreOffice and Mozilla's Firefox are able to use the
Frisian spell checker.


## Word List

The word list in Latin script is in the ASCII file TODO
[`generated/frisian`](generated/frisian).

See the section on installation to make the word lists available as
`/usr/share/dict/frisian` and as symbolic links `/usr/share/dict/frysk` and
`/usr/share/dict/fries`.


## Spell checker

Spell checker support has been made for Hunspell and
[Nuspell](https://nuspell.github.io/). It can be found in the files
[`generated/fy_NL.dic`](generated/fy_NL.dic) and
[`generated/fy_NL.aff`](generated/fy_NL.aff).

See the section on installation to make the spell checker directly available in
Hunspell and Nuspell. It will install the `.aff` and `.dic` files in
`/usr/share/hunspell`. Example usage then is:

    hunspell -d fy_NL -a /usr/share/dict/frisian
    nuspell -d fy_NL /usr/share/dict/frisian

See the test script on how to use the spell checker without installing the
packages. Simply use absolute or relative paths.


## Building

To build, tast and package all the files, simply run the scripts in the
`scripts` directory in their order:
1. `./1-download-language-support.sh`
2. `./2-extract-files.sh`
3. `./3-generate-files.sh` (which calls `3-generate-files.py`)
5. `./4-test-spell-checking.sh` (see the result in directory `test`)
6. `./5-package.sh` (see the result in directory `packages`)

Note to update version number `static/control*` before building a new package.


## See also

The following sources are relevant:
* https://en.wikipedia.org/wiki/West_Frisian_language
* https://en.wikipedia.org/wiki/West_Frisian_alphabet
* https://en.wikipedia.org/wiki/West_Frisian_grammar
* https://en.wikipedia.org/wiki/Fryske_Akademy
* https://fryske-akademy.nl
* https://nuspell.github.io
