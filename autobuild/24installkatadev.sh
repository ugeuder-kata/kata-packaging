#! /bin/sh
# this command from http://rpm5.org/community/rpm-users/0972.html
arch=$(AUTOV=1 rpm -q --qf '%{arch}\n' --specfile rpms/kata-ckan-dev/kata-ckan-dev.spec | head -n 1)
cd rpmbuild/RPMS/${arch}
script -c 'sudo yum install -y kata-ckan-dev-[0-9][0-9][0-9][0-9][0-9][0-9]-1.el6.'${arch}.rpm

