import logging
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes
from ckan.plugins import IGenshiStreamFilter
from ckan.plugins import IConfigurer
from pylons.i18n import _
from genshi.input import HTML
from genshi.filters import Transformer
import html
import json
import os

log = logging.getLogger(__name__)

class iRODSPlugin(SingletonPlugin):
    implements(IGenshiStreamFilter)
    implements(IConfigurer)
    implements(IRoutes)

    def filter(self, stream):
        from pylons import request, tmpl_context as c
        routes = request.environ.get('pylons.routes_dict')
        if routes.get('controller') == 'package' and routes.get('action') == 'resource_read':
            data = {
                    'url':'/irods/%s' % json.loads(c.resource_json)['id']
            }
            stream = stream | Transformer('body//div[@id="minornavigation"]/ul').append(HTML(html.IRODS_PILL%data))
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
        map.connect('irods', '/irods/{id}',
                    controller='ckanext.irods.controllers:iRODSView',
                    action='view')
        return map

    def after_map(self, map):
        return map

    
