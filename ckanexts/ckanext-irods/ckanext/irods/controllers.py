import logging
from ckan.model import Resource, Package
from ckan.model.meta import Session
import ckan.model as model
from ckan.lib.base import BaseController, render, abort
import ckan.lib.helpers as h
from ckan.logic import check_access, NotAuthorized

from pylons import request, tmpl_context as c

log = logging.getLogger(__name__)
def get_connection_from_params(params):
    conn = None
    username = params['uname']
    password = params['pw']
    host = params['server']
    port = params['port']
    zone = params['zone']
    if (host and port and username and zone):
        from irods import rcConnect, clientLoginWithPassword
        conn, _ = rcConnect(host, int(port), username, zone)
        clientLoginWithPassword(conn, password)
    return conn

class iRODSView(BaseController):

    def view(self, id):
        res = Resource.get(id)
        context = {'model':model, 'user': c.user or c.author, 'resource': res }
        try:
            check_access('resource_update', context, {'id' : id})
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))
        if ('save' in request.params):
            sync_irods(request.params, id)
        c.resource_name = res.name
        c.resource_id = res.id
        return render('ckanext/irods/irods.html')

def sync_irods(params, id):
    from irods import getFileUserMetadata
    conn = get_connection_from_params(params)
    resource = Resource.get(id)
    path = params['path']
    if conn:
        for met in getFileUserMetadata(conn, path):
            key, value, _ = met
            resource.extras[key] = value
        Session.add(resource)
        conn.disconnect()
        h.flash_success("iRODS import to resource OK!")
    else:
        h.flash_error("Could not connect to iRODS!")
    h.redirect_to(controller='package', action='resource_read', \
              id=resource.resource_group.package.name, \
              resource_id=resource.id)

class iRODSImport(BaseController):

    def view(self, id):
        context = {'model':model, 'user': c.user or c.author}
        try:
            check_access('package_update', context, {'id' : id})
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))
        pkg = Package.get(id)
        c.pkg = pkg.name
        if ('save' in request.params):
            self.import_irods_collection(request.params, id)
        return render('ckanext/irods/irods.html')

    def import_irods_collection(self, params, id):
        
        from irods import irodsCollection
        path = params['path']
        pkg = Package.get(id)
        conn = get_connection_from_params(params)
        if (conn):
            coll = irodsCollection(conn, path)
            import_collection_to_package(coll, pkg, conn)
            conn.disconnect()
            h.flash_success("iRODS import OK!")
        else:
            h.flash_error("Could not connect to iRODS!")
        h.redirect_to(controller='package', action='read', id=id)

def import_collection_to_package(coll, pkg, conn):
    from irods import iRodsOpen
    rev = model.repo.new_revision()
    log.debug(coll.getCollName())
    for obj in coll.getObjects():
        extras = {} 
        fname, _ = obj
        fname = "%s/%s" % (coll.getCollName(), fname) 
        f = iRodsOpen(conn, fname, 'r')
        log.debug(fname)
        log.debug(f)
        if f:
            for met in f.getUserMetadata():
                key, value, _ = met
                extras[key] = value
                res = Resource.by_name(fname)
                if not res:
                    res = Resource(url = 'irods://%s/%s' % (\
                            coll.getCollName(), str(fname)), \
                            name=fname, extras=extras, \
                            resource_type='file')
                res.extras = extras
            resgrp = pkg.resource_groups[0]
            resgrp.resources.append(res)
            Session.add(res)
            Session.add(resgrp)
    for met in coll.getUserMetadata():
        key, value, _ = met
        pkg.extras[key] = value
    Session.add(pkg)
    model.repo.commit()
