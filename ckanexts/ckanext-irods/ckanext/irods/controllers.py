import logging
from ckan.model import Resource, Package
from ckan.model.meta import Session
import ckan.model as model
from ckan.lib.base import BaseController
from ckan.lib.base import render
import ckan.lib.helpers as h
from pylons import request, tmpl_context as c

log = logging.getLogger(__name__)

class iRODSView(BaseController):

    def view(self, id):
        if ('save' in request.params):
            self.sync_irods(request.params, id)
        res = Resource.get(id)
        c.resource_name = res.name
        c.resource_id = res.id
        return render('ckanext/irods/irods.html')

    def sync_irods(self, params, id):
        username = params['uname']
        password = params['pw']
        host = params['server']
        port = params['port']
        zone = params['zone']
        path = params['path']
        if (host and port and username and zone):
            from irods import rcConnect, clientLoginWithPassword, getFileUserMetadata
            resource = Resource.get(id)
            conn, _ = rcConnect(host, int(port), username, zone)
            clientLoginWithPassword(conn, password)
            if conn:
                for met in getFileUserMetadata(conn, path):
                    key, value, _ = met
                    resource.extras[key] = value
                Session.add(resource)
                conn.disconnect()
                h.flash_success("iRODS import to resource OK!")
            else:
                h.flash_error("Could not connect to iRODS!")
        else:
            h.flash_error("Missing either host, port, username or zone.")
        h.redirect_to(controller='package', action='resource_read', \
                      id=resource.resource_group.package.name, \
                      resource_id=resource.id)

class iRODSImport(BaseController):

    def view(self, id):
        pkg = Package.get(id)
        c.pkg = pkg.name
        if ('save' in request.params):
            self.import_irods_collection(request.params, id)
        return render('ckanext/irods/irods.html')

    def import_irods_collection(self, params, id):
        username = params['uname']
        password = params['pw']
        host = params['server']
        port = params['port']
        zone = params['zone']
        path = params['path']
        if (host and port and username and zone):
            from irods import rcConnect, clientLoginWithPassword, irodsCollection
            pkg = Package.get(id)
            conn, _ = rcConnect(host, int(port), username, zone)
            clientLoginWithPassword(conn, password)
            if (conn):
                coll = irodsCollection(conn, path)
                self._import_collection_to_package(coll, pkg)
                conn.disconnect()
                h.flash_success("iRODS import OK!")
            else:
                h.flash_error("Could not connect to iRODS!")
        else:
            h.flash_error("Missing either host, port, username or zone.")
        h.redirect_to(controller='package', action='read', id=id)

    def _import_collection_to_package(self, coll, pkg):
        for obj in coll.getObjects():
            extras = {}
            fname, rname = obj
            f = coll.open(fname, 'r', rname)
            if f:
                for met in f.getUserMetadata():
                    key, value, _ = met
                    extras[key] = value
                res = Resource.by_name(fname)
                if not res:
                    res = Resource(url = 'irods://%s/%s' % (coll.getCollName(), str(fname)), \
                               name=fname, extras=extras, resource_type='file')
                else:
                    res.extras = extras
                resgrp = pkg.resource_groups[0]
                resgrp.resources.append(res)
                Session.add(res)
                Session.add(resgrp)
        for met in coll.getUserMetadata():
            key, value, _ = met
            pkg.extras[key] = value
        Session.add(pkg)
        rev = model.repo.new_revision()
        model.repo.commit()
