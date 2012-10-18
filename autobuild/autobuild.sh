#! /bin/bash
abuilduser=abuild
abuildkey=~/id_rsa_abuild
abuildhostdev=abuild
abuildhostprod=abuild2
# requirements: access with ssh key $abuildkey must be authorized by 
#               user $abuild
# for further requirements see README

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
    abuildhost=$abuildhostdev
    tar cf abuild.tar .
    scp -i $abuildkey abuild.tar ${abuilduser}@${abuildhost}:
    rexec tar xf abuild.tar
    rexec autobuild/04addrepos.sh
    rexec autobuild/08setuprpmbuild.sh
    rexec autobuild/12buildinstallsolr.sh
    rexec autobuild/16buildmcfg.sh
    rexec autobuild/20buildkatadev.sh
    rexec autobuild/22installmcfgandconfigure.sh
    rexec autobuild/24installkatadev.sh
    $SETCOLOR
    echo "Now test the dev installation"
    $RESETCOLOR ;;
  2)
    abuildhost=$abuildhostdev
    rexec autobuild/28stopservices.sh
    rexec autobuild/32buildkataprod.sh
    rexec autobuild/36tarrpms.sh
    e=$(date +%s)
    min=$(($e/60))
    version=$(($min%1000000))
    scp -i $abuildkey ${abuilduser}@${abuildhost}:rpmbuild/RPMS/rpms.tar rpms-${version}.tar
    $SETCOLOR
    if [ "$abuildhostdev" = "$abuildhostprod" ]
    then
      echo "Reset host $abuild for phase 3"
    else
      echo "Make sure $abuildhostprod has been reset before continuing with phase 3" 
    fi
    $RESETCOLOR ;;

  3)
    abuildhost=$abuildhostprod
    scp -i $abuildkey $(ls rpms-*.tar | tail -1) ${abuilduser}@${abuildhost}:
    rexec mkdir autobuild
    scp -i $abuildkey autobuild/04addrepos.sh ${abuilduser}@${abuildhost}:autobuild/04addrepos.sh
    rexec autobuild/04addrepos.sh
    scp -i $abuildkey autobuild/40installprod.sh ${abuilduser}@${abuildhost}:autobuild/40installprod.sh
    rexec autobuild/40installprod.sh ;;
  *)
    echo "usage: $0 [1|2|3]"
    exit 1 ;;
esac

    
  
