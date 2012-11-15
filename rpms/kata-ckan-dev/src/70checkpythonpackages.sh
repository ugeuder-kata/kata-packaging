#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP70 ]
then
  echo "Skipping 70"
  exit 0
fi
instloc=$1
expected=$2
cd $instloc
source pyenv/bin/activate

SETCOLOR_SUCCESS="echo -en \\033[1;32m"
SETCOLOR_FAILURE="echo -en \\033[1;31m"
SETCOLOR_NORMAL="echo -en \\033[0;39m"
current=/tmp/pip.freeze.current
# need to write to tmp first, because we are not root 
pip freeze >$current
if diff $expected $current >/tmp/kata-70.tmp
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

