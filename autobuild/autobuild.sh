#! /bin/sh
abuilduser=abuild
abuildkey=~/id_rsa_abuild
abuildhost=abuild
# requirements: $abuildkey must be autorized for both uaser $abuild and root

SETCOLOR="echo -en \\033[1;36m"
SETATTENTION="echo -en \\033[1;46m"
RESETCOLOR="echo -en \\033[0m"

function rexec() {
  $SETCOLOR
  echo $*
  $RESETCOLOR
  ssh -i $abuildkey ${abuilduser}@${abuildhost} $*
}

set -x

$SETATTENTION
date
$RESETCOLOR
tar cf abuild.tar .
scp -i $abuildkey abuild.tar ${abuilduser}@${abuildhost}:
rexec tar xf abuild.tar
rexec autobuild/04addrepos.sh
rexec autobuild/08setuprpmbuild.sh
rexec autobuild/12buildinstallsolr.sh
rexec autobuild/16buildmcfg.sh
rexec autobuild/20buildkatadev.sh
rexec autobuild/24installkatadev.sh
