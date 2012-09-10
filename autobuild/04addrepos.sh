#! /bin/sh
sudo yum install -y wget
wget http://www.nic.funet.fi/pub/mirrors/fedora.redhat.com/pub/epel/6/i386/epel-release-6-7.noarch.rpm
sudo rpm -i epel-release-6-7.noarch.rpm