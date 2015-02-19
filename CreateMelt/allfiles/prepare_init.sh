#!/bin/bash

if [ -z "$1" ]
then
  echo " the program creates a init.data file and copies in.* files in the current directory"
  echo "usage:  prepare_init.sh inputfile(ex: def.chain) | the result is  outputfile(init.data)"
  exit 1
fi

chain.out < $1 > init.data
CURRENT=`pwd`
curdir="echo $CURRENT/"
cp ~/lammpsfiles/in.* ./


