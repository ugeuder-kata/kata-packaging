#!/bin/sh
cp /etc/shibboleth/shibboleth2.xml /etc/shibboleth/shibboleth2.xml.orig
cp /etc/shibboleth/attribute-map.xml /etc/shibboleth/attribute-map.xml.orig
cp /usr/share/kata-ckan-dev/setup-data/attribute-map.xml /etc/shibboleth/attribute-map.xml

cp /etc/shibboleth/attribute-policy.xml /etc/shibboleth/attribute-policy.xml.orig
cp /usr/share/kata-ckan-dev/setup-data/attribute-policy.xml /etc/shibboleth/attribute-policy.xml
