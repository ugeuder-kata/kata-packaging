#! /bin/sh
set -x
if [ -f /tmp/kata-SKIP20 ]
then
  echo "Skipping 20"
  exit 0
fi
patchdir="$1"
# customer wants database to be stored under /opt/data
#
# 1. Observations:
#
# postgresql-server package installation creates 3 directories and 1 file:
#
# /var/lib/pgsql
# /var/lib/pgsql/.bash_profile
# /var/lib/pgsql/backups
# /var/lib/pgsql/data
#
# (actually /var/lib/pgsql is the home directory of the postgres user account)
#
# Command "service postgresql initdb" populates the data directory (both with
# configuration files and database contents). A small log file is located
# directly in /var/lib/pgsql
#
# unistalling the package removes only the .bash_profile but nothing else
#
# 2. Design
#
# Our solution: replace /var/lib/pgsql by a symbolic link to /opt/data/pgsql

if [ -L /var/lib/pgsql ]
then
  # assume that if postgres' home directory is symbolic link we already have
  # a valid CKAN DB and want to preserve it
  echo "Existing database link found, don't initialize Postgres DB"
  touch /tmp/kata-SKIP-dbinit
  service postgresql start
  exit 0
else
  rm -f /tmp/kata-SKIP-dbinit 2>/dev/null
fi

# handle the alternate storage location
mkdir -p /opt/data/pgsql
chown postgres:postgres /opt/data/pgsql/
chmod og= /opt/data/pgsql/
mv /var/lib/pgsql/.bash_profile /var/lib/pgsql/* /opt/data/pgsql/
ln -s /opt/data/pgsql /var/lib/pgsql
# link is now owned by root, that should not matter
# alternate storage location done, continue as nothing had happened

service postgresql initdb
pushd /var/lib/pgsql/data >/dev/null
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
