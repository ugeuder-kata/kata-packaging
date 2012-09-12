#! /bin/sh
abuilduser=abuild
abuildkey=~/id_rsa_abuild
abuildhost=abuild
# requirements: $abuildkey must be autorized for both uaser $abuild and root

function rexec() {
  ssh -i $abuildkey ${abuilduser}@${abuildhost} $*
}

set -x

tar cf abuild.tar .
scp -i $abuildkey abuild.tar ${abuilduser}@${abuildhost}:
rexec tar xf abuild.tar
rexec autobuild/04addrepos.sh
rexec autobuild/08setuprpmbuild.sh
rexec autobuild/12buildsolr.sh
rexec autobuild/16buildmcfg.sh
rexec autobuild/20buildkatadev.sh
rexec autobuild/24installkatadev.sh
