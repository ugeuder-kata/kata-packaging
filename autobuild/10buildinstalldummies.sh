#! /bin/sh
cd rpms/dummy-deps
./build-from-repo.sh
arch=$(AUTOV=foo rpm -q --qf '%{arch}\n' --specfile dummy-deps.spec | head -n 1)
cd ~/rpmbuild/RPMS/${arch}
sudo yum install -y dummy-deps-[0-9][0-9][0-9][0-9][0-9][0-9]-1.el?.${arch}.rpm
