#!/bin/sh
cert=""
ok=false
shibboleth="/etc/shibboleth";
wayf_metadata_filename="wayf-metadata.xml";
wayf_metadata_file="/tmp/$wayf_metadata_filename"; # Path to save WAYF metadata.xml
wayf_metaurl="https://haka.funet.fi/metadata/haka_test_metadata_signed.xml" # WAYF metadata URL
wayf="https://testsp.funet.fi/shibboleth/WAYF" # WAYF URL, where users are redirected from SP
fqdn="my.sp.domain.com" # SP machine domain name



# Certificate file
while ! $ok; do
    read -p "Certificate [/etc/pki/tls/certs/ca.crt]: " cert

	if [ -f "$cert" ]; then
		ok=true;
	fi
done

# Shibboleth SP FQDN
read -p "Shibboleth SP FQDN [$fqdn]: " input
if [ "$input" != "" ]; then
	fqdn="$input"
fi

# WAYF/DS
read -p "Shibboleth WAYF/DS [$wayf]: " input
if [ "$input" != "" ]; then
	wayf="$input"
fi

# WAYF/DS metadata URL
read -p "WAYF/DS metadata URL [$wayf_metaurl]: " input
if [ "$input" != "" ]; then
	wayf_metaurl="$input"
fi

curl $wayf_metaurl > $wayf_metadata_file;


echo "Shibboleth SP domain: $fqdn"
echo "Certificate file: $cert"
echo "Shibboleth WAYF/DS name: $wayf"
echo "Shibboleth WAYF/DS metadata: $wayf_metaurl"
echo "Shibboleth WAYF/DS metadata file: $wayf_metadata_file"
