#! /bin/sh
abuilduser=$1
set -x
eval rpm -i ~${abuilduser}/epel-release-6-7.noarch.rpm
