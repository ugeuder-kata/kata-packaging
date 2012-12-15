#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP12 ]
then
  echo "Skipping 12"
  exit 0
fi
instloc=$1
cd $instloc
source pyenv/bin/activate
if [ -r /etc/kata-ckan-dev/versions ]
then
   source /etc/kata-ckan-dev/versions
else
   ckan_version=
fi
theirurl='git+https://github.com/okfn/ckan.git'
oururl='git+https://github.com/kata-csc/ckan.git'
pip install -e ${oururl}${ckan_version}#egg=ckan
pip install -r pyenv/src/ckan/pip-requirements.txt
# according to installation instructions we need to deactive our pyenv here
# will happen automatically because script ends here
