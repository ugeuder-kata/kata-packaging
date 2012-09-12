#! /bin/sh
sudo yum install -y wget
wget http://www.nic.funet.fi/pub/mirrors/fedora.redhat.com/pub/epel/6/i386/epel-release-6-7.noarch.rpm
sudo yum install -y epel-release-6-7.noarch.rpm
wget http://download.opensuse.org/repositories/security://shibboleth/CentOS_CentOS-6/security:shibboleth.repo
sudo cp security:shibboleth.repo /etc/yum.repos.d/
