#!/bin/sh

IDP_PATH=/opt/shibboleth-idp
SP_PATH=/etc/shibboleth
TOMCAT_BIN=/usr/local/tomcat/bin

service httpd stop
service shibd stop
sh $TOMCAT_BIN/shutdown.sh

sleep 10

rm -f $IDP_PATH/logs/*
rm -f /var/log/shibboleth/*
rm $IDP_PATH/metadata/sp-metadata.xml
rm /var/run/shibboleth/idp-metadata.xml

sh $TOMCAT_BIN/startup.sh
service shibd start
service httpd start
