#!/bin/bash

IP=192.168.1.120
IDP_PATH=/opt/shibboleth-idp
SP_PATH=/etc/shibboleth
TOMCAT_BIN=/usr/local/tomcat/bin

sh $TOMCAT_BIN/shutdown.sh
service shibd stop

sleep 5

rm -f $IDP_PATH/logs/*
rm $IDP_PATH/metadata/sp-metadata.xml
rm /var/run/shibboleth/idp-metadata.xml

#sh $SP_PATH/metagen.sh -c $SP_PATH/sp-cert.pem -h $IP -e https://$IP/shibboleth-sp > /var/www/sp-metadata.xml

cp $IDP_PATH/metadata/idp-metadata.xml /var/www/

sh $TOMCAT_BIN/startup.sh
service shibd start
