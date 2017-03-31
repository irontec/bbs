# Black Box SIP

Black Box SIP is a simple User Agent simulator for testing SIP PBX and Proxies
only based on their sent inputs and expected outputs.

## Requirements

- python (2.7+)
- pjsua-python (python bindings for pjproject libraries)
- clint

## Installation

On most systems you can use setup.py script to build and install BBS

```
$ python setup.py build
# python setup.py install
```

## Usage

BBS reads a configuration YAML file with the information of the scenarios to
execute. Check examples directory for some basic UAC->UAS examples.
You can also specify credentials in another extra confgiration file.

BBS supports output in JUnit for reporting in continous intragration engines.

```
bbs -c examples/simple.yaml -e credentials.yaml -vvv -k -o results.xml
```

## License
```
bbs - Black Box SIP tester
Copyright (C) 2013-2016 Irontec S.L.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

In addition, as a special exception, the copyright holders give
permission to link the code of portions of this program with the
OpenSSL library under certain conditions as described in each
individual source file, and distribute linked combinations
including the two.
You must obey the GNU General Public License in all respects
for all of the code used other than OpenSSL.  If you modify
file(s) with this exception, you may extend this exception to your
version of the file(s), but you are not obligated to do so.  If you
do not wish to do so, delete this exception statement from your
version.  If you delete this exception statement from all source
files in the program, then also delete it here.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
