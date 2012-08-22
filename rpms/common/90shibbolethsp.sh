#!/bin/sh
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/shibboleth2.xml.patch
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/attribute-map.xml.patch
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/attribute-policy.xml.patch
