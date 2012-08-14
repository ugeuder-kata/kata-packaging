#! /bin/sh
set -x
service httpd restart
chkconfig httpd on
chown -R ckan:apache /home/ckan/pyenv
chmod -R 755 /home/ckan
setsebool -P httpd_can_network_connect 1
chcon -R --type=httpd_sys_content_t /home/ckan
touch /home/ckan/pyenv/ckan.log
chown ckan:apache /home/ckan/pyenv/ckan.log
chmod g+w /home/ckan/pyenv/ckan.log
chmod -R g+w /home/ckan/pyenv/src/ckan/{data,sstore}
sed -i 's/CFUNCTYPE(c_int)(lambda: None)/#CFUNCTYPE(c_int)(lambda: None)/' /usr/lib64/python2.6/ctypes/__init__.py