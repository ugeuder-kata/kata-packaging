#! /bin/sh
e=$(date +%s)
min=$(($e/60))
version=$(($min%1000000))
if [ -d kata-ckan-dev-${version} ]
# not very likely, but who cares...
then
  rm -rf kata-ckan-dev-${version}
fi
cp -a src kata-ckan-dev-${version}
tar cjf kata-ckan-dev-${version}.tgz kata-ckan-dev-${version}/
rm -rf kata-ckan-dev-${version}
here=$(pwd)
pushd ~/rpmbuild >/dev/null
cd SPECS
if [ -L kata-ckan-dev.spec ]
then
  rm kata-ckan-dev.spec
fi
ln -s ${here}/kata-ckan-dev.spec
cd ../SOURCES
if [ -L kata-ckan-dev-${version}.tgz ]
# not very likely, but who cares...
then
  rm kata-ckan-dev-${version}.tgz ]
fi
ln -s ${here}/kata-ckan-dev-${version}.tgz
cd ..
AUTOV=${version} rpmbuild -ba SPECS/kata-ckan-dev.spec
rm SPECS/kata-ckan-dev.spec
rm SOURCES/kata-ckan-dev-${version}.tgz
popd >/dev/null
rm kata-ckan-dev-${version}.tgz


