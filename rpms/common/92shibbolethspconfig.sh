#!/bin/sh
cert="/etc/pki/tls/certs/ca.crt"
shibboleth="/etc/shibboleth";
wayf_metadata_filename="wayf-metadata.xml";
wayf_metadata_file="$shibboleth/$wayf_metadata_filename"; # Path to save WAYF metadata.xml
wayf_metaurl="https://haka.funet.fi/metadata/haka_test_metadata_signed.xml" # WAYF metadata URL
wayf="https://testsp.funet.fi/shibboleth/WAYF" # WAYF URL, where users are redirected from SP
fqdn="kata-test1.csc.fi" # SP machine domain name

curl $wayf_metaurl > $wayf_metadata_file;

echo "Shibboleth SP domain: $fqdn"
echo "Certificate file: $cert"
echo "Shibboleth WAYF/DS name: $wayf"
echo "Shibboleth WAYF/DS metadata: $wayf_metaurl"
echo "Shibboleth WAYF/DS metadata file: $wayf_metadata_file"
