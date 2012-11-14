#! /bin/sh
psql -c "\d" ckantest | sed "s/[^|]*| \([^|]*\) |.*/\1/" | tail -n +4 | head -n -2 | while read table
do
 psql -c "\d+ ${table}" ckantest
done
