#!/bin/bash
#
# Spustí všechny testy v adresáři: 
#
# author: ivo@wikidi.com

BASEDIR=$(dirname $0)
echo $BASEDIR

run-parts -v --regex 'test_.*\.py' $BASEDIR
