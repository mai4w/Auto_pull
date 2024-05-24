#!/bin/bash

# create important.file
ls /etc/{passwd,shadow,group} > important.file
find /usr/sbin /usr/bin -perm /6000 >> important.file

# list md5sum for important file
for filename in $(cat important.file)
do
  md5sum $filename >> finger1.file
done

# rm important file
rm -f important.file
