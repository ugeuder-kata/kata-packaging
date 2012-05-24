#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP02 ]
then
  echo "Skipping 02"
  exit 0
fi
instloc=$1
cd $instloc
source pyenv/bin/activate
pip install --ignore-installed -e git+https://github.com/okfn/ckan.git#egg=ckan
pip install --ignore-installed -r pyenv/src/ckan/requires/lucid_missing.txt -r pyenv/src/ckan/requires/lucid_conflict.txt
pip install webob==1.0.8
pip install --ignore-installed -r pyenv/src/ckan/requires/lucid_present.txt
echo "TODO: Cython not yet used"
# according to installation instructions we need to deactive our pyenv here
# will happen automatically because script ends here
