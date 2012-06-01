"""
Plugin implementation for iRODS import for CKAN.
"""
import logging
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes
from ckan.plugins import IGenshiStreamFilter
from ckan.plugins import IConfigurer
from ckan.plugins import IAuthorizer
from genshi.input import HTML
from genshi.filters import Transformer
import html
import json
import os
import re

log = logging.getLogger(__name__)

class iRODSPlugin(SingletonPlugin):
    """
    This plugin needs to modify the code for dataset and resource view, so a
    IGenshiStreamFilter is implemented. Also to configure the custom templates
    to a path in the plugin directory, we need IConfigurer. Lastly, to display
    the forms for import, we need to define routes for them, hence the IRoutes
    interface is implemented.
    """
    implements(IGenshiStreamFilter)
    implements(IConfigurer)
    implements(IRoutes)

    def filter(self, stream):
        """
        Modify dataset and resource view on the fly and add a link to the "pills"
        in the html templates, which are basically menuitems.
        """
        from pylons import request, tmpl_context as c
        routes = request.environ.get('pylons.routes_dict')
        if routes.get('controller') == 'package' and routes.get('action') == \
                                                    'resource_read':
            data = {
                    'url':'/irods/%s' % json.loads(c.resource_json)['id']
            }
            stream = stream | Transformer('body//div[@id="minornavigation"]/ul')\
                                .append(HTML(html.IRODS_PILL%data))
        elif routes.get('controller') == 'package' and routes.get('action') == \
                                                        'read':
            data = {
                    'url':'/irods_import/%s' % c.current_package_id
            }
            stream = stream | Transformer('body//div[@id="minornavigation"]/ul')\
                                .append(HTML(html.IRODS_PILL%data))
        return stream

    def update_config(self, config):
        """This IConfigurer implementation causes CKAN to look in the
        ```public``` and ```templates``` directories present in this
        package for any customisations.

        It also shows how to set the site title here (rather than in
        the main site .ini file), and causes CKAN to use the
        customised package form defined in ``package_form.py`` in this
        directory.
        """
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        template_dir = os.path.join(rootdir, 'ckanext',
                                    'irods', 'templates')
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])

    def before_map(self, map):
        """
        Map our controllers to separate urls.
        """
        map.connect('irods', '/irods/{id}',
                    controller='ckanext.irods.controllers:iRODSView',
                    action='view')
        map.connect('irods_import', '/irods_import/{id}',
                    controller='ckanext.irods.controllers:iRODSImport',
                    action='view')
        return map

    def after_map(self, map):
        """
        Nothing to do here.
        """
        return map

class iRODSAuthorization(SingletonPlugin):
    """
    Checks for authorization information for a dataset/resource from iRODS.
    """
    implements(IAuthorizer)

    def is_authorized(self, username, action, domain_obj):
        """
        Check if a user exists in iRODS, if it does, check if there is access
        to the collection/file.
        """
        log.debug(domain_obj)
        log.debug(action)
        log.debug(username)
        ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" #pylint: disable-msg=C0301
        log.debug(re.match(ValidIpAddressRegex, username))
        if re.match(ValidIpAddressRegex, username) != None:
            log.debug("FALSE")
            return False
        if username:
            log.debug("TRUE")
            return True
    def get_authorization_groups(self, username):
        """
        No groups to append.
        """
        return []
    def get_roles(self, username):
        """
        No roles to append.
        """
        return []
