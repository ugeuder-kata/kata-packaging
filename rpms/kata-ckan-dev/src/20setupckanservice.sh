#! /bin/sh
set -x
service ckan-dev start
chkconfig ckan-dev on
