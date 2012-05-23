#! /bin/sh
service postgresql initdb
pushd /var/lib/pgsql/data >/dev/null
patch -p2 -i /usr/share/kata-ckan-dev/setup-patches/pg_hba.conf.patch
popd >/dev/null
service postgresql start

