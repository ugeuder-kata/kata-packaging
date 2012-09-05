#!/bin/sh
cert="/etc/pki/tls/certs/ca.crt"
shibboleth="/tmp";
wayf_metadata_filename="wayf-metadata.xml";
wayf_metadata_file="$shibboleth/$wayf_metadata_filename"; # Path to save WAYF metadata.xml
wayf_metaurl="https://haka.funet.fi/metadata/haka_test_metadata_signed.xml" # WAYF metadata URL
wayf="https://testsp.funet.fi/shibboleth/WAYF" # WAYF URL, where users are redirected from SP
SP_FQDN="kata-test1.csc.fi" # SP machine domain name

SpKey="sp-key.pem"		# default: /etc/shibboleth/sp-key.pem
SpCert="sp-cert.pem"	# default: /etc/shibboleth/sp-cert.pem
sed -i "s/%%SpKey%%/${SpKey}/g" "$shibboleth/shibboleth2.xml"
sed -i "s/%%SpCert%%/${SpCert}/g" "$shibboleth/shibboleth2.xml"


# Application defaults
entityID="https://sp.example.com/shibboleth"
REMOTE_USER="eppn persistent-id targeted-id"
ApplicationDefaults='<ApplicationDefaults entityID="%%entityID%%" REMOTE_USER="%%REMOTE_USER%%">'
sed -i "s/%%ApplicationDefaults%%/${ApplicationDefaults}/g" "$shibboleth/shibboleth2.xml";
echo "-------------"
cat /tmp/shibboleth2.xml |grep %%entityID%%
echo "-------------"
sed -i "s-%%entityID%%-${entityID}-g" "$shibboleth/shibboleth2.xml";
sed -i "s-%%REMOTE_USER%%-${REMOTE_USER}-g" "$shibboleth/shibboleth2.xml";

# SSO Session element
SSO='<SSO discoveryProtocol="WAYF" discoveryURL="%%WAYF_URL%%">SAML2 SAML1</SSO>'
sed -i "s/%%SSO%%/${SSO}/g" "$shibboleth/shibboleth2.xml"
sed -i "s/%%WAYF_URL%%/${wayf}/g" "$shibboleth/shibboleth2.xml"

# Handler
Handler_type_Status='<Handler type="Status" Location="/Status" acl="%%SP_FQDN%%"/>'
sed -i "s/%%Handler_type_Status%%/${Handler_type_Status}/g" "$shibboleth/shibboleth2.xml"
sed -i "s/%%SP_FQDN%%/${SP_FQDN}/g" "$shibboleth/shibboleth2.xml"

# MetadataProvider
MetadataProvider=$(cat <<EOF
<MetadataProvider type="XML" uri="$wayf_metaurl"
	backingFilePath="$wayf_metadata_filename" reloadInterval="7200">
</MetadataProvider>
EOF
)
sed -i "s/%%MetadataProvider%%/${MetadataProvider}/g" "$shibboleth/shibboleth2.xml"

curl $wayf_metaurl > $wayf_metadata_file;

