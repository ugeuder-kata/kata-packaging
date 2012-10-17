#! /bin/sh
abuilduser=abuild
abuildkey=~/id_rsa_abuild
abuildhostdev=abuild
abuildhostprod=abuild2
abuildhostdevport=22
abuildhostprodport=22
if [ \! -z "$ABUILDHOST" ]
then
  abuildhostdev=$ABUILDHOST
  abuildhostprod=$ABUILDHOST
fi
if [ \! -z "$ABUILDHOSTDEV" ]
then
  abuildhostdev=$ABUILDHOSTDEV
fi
if [ \! -z "$ABUILDHOSTPROD" ]
then
  abuildhostprod=$ABUILDHOSTPROD
fi
if [ \! -z "$ABUILDPORT" ]
then
  abuildportdev=$ABUILDPORT
  abuildportprod=$ABUILDPORT
fi
if [ \! -z "$ABUILDPORTDEV" ]
then
  abuildportdev=$ABUILDPORTDEV
fi
if [ \! -z "$ABUILDPORTPROD" ]
then
  abuildportprod=$ABUILDPORTPROD
fi
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
  ssh -i $abuildkey -p $abuildport ${abuilduser}@${abuildhost} $*
}

set -x

$SETATTENTION
date
$RESETCOLOR
case $phase in
  1)
    abuildhost=$abuildhostdev
    abuildport=$abuildportdev
    tar cf abuild.tar .
    scp -i $abuildkey -P $abuildport abuild.tar ${abuilduser}@${abuildhost}:
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
    abuildport=$abuildportdev
    rexec autobuild/28stopservices.sh
    rexec autobuild/32buildkataprod.sh
    rexec autobuild/36tarrpms.sh
    e=$(date +%s)
    min=$(($e/60))
    version=$(($min%1000000))
    scp -i $abuildkey -P $abuildport ${abuilduser}@${abuildhost}:rpmbuild/RPMS/rpms.tar rpms-${version}.tar
    $SETCOLOR
    if [ "$abuildhostdev" = "$abuildhostprod" -a "$abuildportdev" = "$abuildportprod"]
    then
      echo "Reset host ${abuildhost}:${abuildport} for phase 3"
    else
      echo "Make sure ${abuildhostprod}:${abuildportprod} has been reset before continuing with phase 3" 
    fi
    $RESETCOLOR ;;

  3)
    abuildhost=$abuildhostprod
    abuildport=$abuildportprod
    scp -i $abuildkey -P $abuildport $(ls rpms-*.tar | tail -1) ${abuilduser}@${abuildhost}:
    rexec mkdir autobuild
    scp -i $abuildkey -P $abuildport autobuild/04addrepos.sh ${abuilduser}@${abuildhost}:autobuild/04addrepos.sh
    rexec autobuild/04addrepos.sh
    scp -i $abuildkey -P $abuildport autobuild/40installprod.sh ${abuilduser}@${abuildhost}:autobuild/40installprod.sh
    rexec autobuild/40installprod.sh ;;
  *)
    echo "usage: $0 [1|2|3]"
    exit 1 ;;
esac

    
  
