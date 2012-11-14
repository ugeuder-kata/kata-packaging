#! /bin/sh
case "$1" in
  admin) 
    user="$2"
    # known problem with the following command: works only for existing users
    # for non-existing ones prompting will fail because stdin is a here
    # document
    cmd="--plugin=ckan sysadmin add $user --config=development.ini"
    ;;
  reindex)
    cmd="--plugin=ckan search-index rebuild --config=development.ini"
    ;;
  cmd)
    shift
    cmd="$*"
    ;;
  *)
    echo "Usage: $0 <operation> [<param>...]"
    echo 
    echo "   Where <operation> is one of:"
    echo 
    echo "      1.) admin   --- gives sysadmin rights to existing user"
    echo "                      1 mandatory parameter: user id"
    echo "      2.) reindex --- rebuild search index from scratch"
    echo "                      no parameters"
    echo "      3.) cmd     --- any paster command"
    echo "                      command is passed as parameter(s)"
    exit
  esac 
sudo -s -u ckan <<EOF
cd
cd pyenv
source bin/activate
cd src/ckan
paster $cmd
EOF
