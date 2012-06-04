#! /bin/sh
set -x
service postgresql initdb
pushd /var/lib/pgsql/data >/dev/null
# sudo postgres ensures that the resulting file has the correct owner
sudo -u postgres patch -p2 -i /usr/share/kata-ckan-dev/setup-patches/pg_hba.conf.patch
popd >/dev/null
service postgresql start
chkconfig postgresql on
# following command from "postgres createuser -e -S -D -R -P ckanuser"
# couldn't find a way to avoid prompting for the password
cmd="CREATE ROLE ckanuser PASSWORD 'md5372712b8c6097730c3164ddd4f9275e0' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN"
su -c 'psql -c "'"$cmd"'"' postgres
su -c "createdb -O ckanuser ckantest" postgres
