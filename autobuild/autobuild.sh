#! /bin/sh
abuilduser=abuild
abuildkey=~/id_rsa_abuild
abuildhost=abuild
# requirements: $abuildkey must be autorized for both uaser $abuild and root

function rexec() {
  ssh -i $abuildkey ${abuilduser}@${abuildhost} $*
}

function rrexec() {
  ssh -i $abuildkey root@${abuildhost} $*
}

set -x

tar cf abuild.tar .
scp -i $abuildkey abuild.tar ${abuilduser}@${abuildhost}:
rexec tar xf abuild.tar
rrexec yum install -y wget
rexec autobuild/04addrepos.sh
rrexec "~${abuilduser}/autobuild/05addrepos-root.sh" $abuilduser
rexec autobuild/08setuprpmbuild.sh

