#! /bin/sh
abuilduser=abuild
abuildkey=~/id_rsa_abuild
abuildhost=abuild
# requirements: $abuildkey must be authorized for both $abuild

phase=$1

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
case $phase in
  1)
    tar cf abuild.tar .
    scp -i $abuildkey abuild.tar ${abuilduser}@${abuildhost}:
    rexec tar xf abuild.tar
    rexec autobuild/04addrepos.sh
    rexec autobuild/08setuprpmbuild.sh
    rexec autobuild/12buildinstallsolr.sh
    rexec autobuild/16buildmcfg.sh
    rexec autobuild/20buildkatadev.sh
    rexec autobuild/24installkatadev.sh
    $SETCOLOR
    echo "Now test the dev installation"
    $RESETCOLOR ;;
  2)
    rexec autobuild/28stopservices.sh
    rexec autobuild/32buildkataprod.sh
    rexec autobuild/36tarrpms.sh
    e=$(date +%s)
    min=$(($e/60))
    version=$(($min%1000000))
    scp -i $abuildkey ${abuilduser}@${abuildhost}:rpmbuild/RPMS/rpms.tar rpms-${version}.tar
  3)
    echo "install prod" ;;
  *)
    echo "usage: $0 [1|2|3]"
    exit 1 ;;
esac

    
  
