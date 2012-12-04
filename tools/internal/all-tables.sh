#! /bin/sh
psql -c "\d" ckandb | sed "s/[^|]*| \([^|]*\) |.*/\1/" | tail -n +4 | head -n -2 | while read table
do
 psql -c "\d+ ${table}" ckandb
done
