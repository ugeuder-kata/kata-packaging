#! /bin/sh
#
# move those subdirectories we have created ourselves to backup location
# leave other files alone and print a warning
#
instloc=$1
backup=/tmp/uninstall-$(date +%y%m%d-%H%M%S)
mkdir $backup
mv ${instloc}/download ${backup}/
mv ${instloc}/pyenv ${backup}/
left=$(find ${instloc}/ | wc -l)
left=$(($left-1))
if [ $left -ne 0 ]
then
  echo "$left unknown files/directories left in $instloc"
fi
echo "previously installed files moved from $instloc to $backup"
echo "consider running sudo rm -rf $backup"
