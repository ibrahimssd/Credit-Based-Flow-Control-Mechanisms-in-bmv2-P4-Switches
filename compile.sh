#!/bin/bash
echo "compiling the code in process  ..."
rm -rf build/*;
p4c  $1 -o build

