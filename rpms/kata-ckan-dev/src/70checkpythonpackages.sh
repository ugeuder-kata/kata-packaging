#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
instloc=$1
expected=$2
cd $instloc
source pyenv/bin/activate

SETCOLOR_SUCCESS="echo -en \\033[1;32m"
SETCOLOR_FAILURE="echo -en \\033[1;31m"
SETCOLOR_NORMAL="echo -en \\033[0;39m"
if pip freeze | diff - $expected >/tmp/kata-70.tmp
then
  $SETCOLOR_SUCCESS
  echo "Python packages checked OK." 
else
  $SETCOLOR_FAILURE
  echo "Python package mismatches:"
  cat /tmp/kata-70.tmp
fi
$SETCOLOR_NORMAL
rm -f /tmp/kata-70.tmp

