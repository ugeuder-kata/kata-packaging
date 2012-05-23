#! /bin/sh
e=$(date +%s)
min=$(($e/60))
version=$(($min%1000000))
mkdir kata-ckan-dev-${version}
cp src/* kata-ckan-dev-${version}
tar cjz kata-ckan-dev-${version}.tgz kata-ckan-dev-${version}/
rm -rf kata-ckan-dev-${version}
here=$(pwd)
pushd ~/rpmbuild
cd SPEC
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
AUTOV=${version} rpmbuild -ba SPEC/kata-ckan-dev.spec
rm SPEC/kata-ckan-dev.spec
rm SOURCES/kata-ckan-dev-${version}.tgz
popd
rm kata-ckan-dev-${version}.tgz


