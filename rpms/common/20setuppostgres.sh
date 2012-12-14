#! /bin/sh
set -x
if [ -f /tmp/kata-SKIP20 ]
then
  echo "Skipping 20"
  exit 0
fi
patchdir="$1"
# postgresql-server rpm creates 2 directories under the default location:
# data and backups
# let's do the same under our custom location
if [ \! -e /opt/data/pgsql ]
then
  mkdir -p /opt/data/pgsql/data
  mkdir /opt/data/pgsql/backups
  chown -R postgres:postgres /opt/data/pgsql
  chmod -R og= /opt/data/pgsql
fi
pushd /opt/data/pgsql/data >/dev/null
datafiles=$(ls | wc -l)
if [ $datafiles -ne 0 ]
then
  # assume that if there is any DB configuration, it is a valid CKAN DB
  # this is of course not really true
  echo "some database configuration found, don't overwrite it"
  touch /tmp/kata-SKIP-dbinit
  service postgresql start
  exit 0
else
  rm -f /tmp/kata-SKIP-dbinit 2>/dev/null
fi
service postgresql initdb
# su postgres ensures that the resulting file has the correct owner
su -c "patch -b -p2 -i ${patchdir}/pg_hba.conf.patch" postgres
popd >/dev/null
service postgresql start
chkconfig postgresql on
# following command from "postgres createuser -e -S -D -R -P ckanuser"
# couldn't find a way to avoid prompting for the password
cmd="CREATE ROLE ckanuser PASSWORD 'md5372712b8c6097730c3164ddd4f9275e0' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN"
sleep 3    # following psql happened to fail sometimes, wait a moment 
su -c 'psql -c "'"$cmd"'"' postgres
su -c "createdb -O ckanuser ckandb" postgres
