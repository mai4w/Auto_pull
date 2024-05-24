#!/bin/bash

# check if finger1.file exist
if [ ! -f finger1.file ]; then
  echo "Can't fine the finger1.file!"
  echo "Please use the script \"./1-list_important.file.sh\" to create finger1.file!"
  exit 1
fi

# Compare "saved list" with "daily list"
[ -f finger_new.file ] && rm finger_new.file
ls /etc/{passwd,shadow,group} > important_new.file
find /usr/sbin /usr/bin -perm /6000 >> important_new.file
for filename in $(cat important_new.file)
do
  md5sum $filename >> finger_new.file
done
rm -f important_new.file

# Print difference in /var/xxx/xxx/root
CHECK=$(diff finger1.file finger_new.file)
if [ "$CHECK" != "" ]; then
  ORIG_MD5=$(diff finger1.file finger_new.file | grep "^<")
  NEW_MD5=$(diff finger1.file finger_new.file | grep "^>")
  echo "Original file:"
  echo "$ORIG_MD5"
  echo "-"
  echo "Something changed:"
  echo "$NEW_MD5"
fi
