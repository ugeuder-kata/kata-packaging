import logging
from ckan.model import Resource
from ckan.model.meta import Session

from ckan.lib.base import BaseController
from ckan.controllers.api import ApiController
from ckan.lib.base import render, redirect_to
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

class iRODSView(BaseController):

    def view(self, id):
        from pylons import request, tmpl_context as c
        if ('save' in request.params):
            self.sync_irods(request.params)
        res = Resource.get(id)
        c.resource_name = res.name
        c.resource_id = res.id
        return render('ckanext/irods/irods.html')

    def sync_irods(self, params):
        log.debug(params)
        username = params['uname']
        password = params['pw']
        host = params['server']
        port = params['port']
        from irods import rcConnect, clientLoginWithPassword, getFileUserMetadata
        resource = Resource.get(params['resource'])
        dataset = params['dataset']
        conn, _ = rcConnect(host, int(port), username, 'omaZone')
        clientLoginWithPassword(conn, password)
        rescpath = '/omaZone/home/'+username+'/'+resource.name.split('/')[-1]
        log.debug(rescpath)
        for met in getFileUserMetadata(conn, rescpath):
            attr1, attr2, _ = met
            log.debug(attr1)
            log.debug(attr2)
            resource.extras[attr1] = attr2
        Session.add(resource)
        conn.disconnect()
        h.redirect_to(controller='package', action='resource_read', id=resource.resource_group.package.name, resource_id=resource.id)

