#! /bin/sh
set -x
patchdir="$1"
service httpd stop
pushd /etc/httpd/conf >/dev/null
patch -b -p2 -i ${patchdir}/httpd.conf.patch
mv httpd.conf httpd.conf.step1
myipcmd=$(dirname $0)/myip.sh
myip=$($myipcmd)
sed -e "s/%%MYIP%%/${myip}/" httpd.conf.step1 > httpd.conf
popd >/dev/null
chkconfig httpd on
chown -R ckan:apache /home/ckan/pyenv
chmod -R 755 /home/ckan
setsebool -P httpd_can_network_connect 1
chcon -R --type=httpd_sys_content_t /home/ckan
touch /home/ckan/pyenv/ckan.log
chown ckan:apache /home/ckan/pyenv/ckan.log
chmod g+w /home/ckan/pyenv/ckan.log
chmod -R g+w /home/ckan/pyenv/src/ckan/{data,sstore}
# TODO: We should not hack other packages' files
# what will happen when Python gets a security update???
# well, as long as we do it only in dev it doesn't matter, because
# dev systems does not live very long
for dir in $(echo /usr/lib*/python2.6)
# loop exists to handle both 32 and 64 bit installations. Not sure whether
# it could ever be run more than once, but that doesn't matter 
do
  sed -i.orig 's/CFUNCTYPE(c_int)(lambda: None)/#CFUNCTYPE(c_int)(lambda: None)/' ${dir}/ctypes/__init__.py
done