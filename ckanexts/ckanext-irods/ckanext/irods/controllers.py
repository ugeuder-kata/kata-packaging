#pylint: disable-msg=E1101,E0602
"""
Controllers for iRODS plugin.
"""
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
    """
    Create a iRODS data connection from POST parameters.
    """
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
    """
    Controller for resource based imports.
    """
    def view(self, id):
        """
        Renders a form for iRODS resource import, if it receives a POST request,
        it simply calls sync_irods function in order to do the actual import.
        """
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
    """
    Fetches a resource from database with the same path as user specified and 
    that matches an existing resource in CKAN.
    """
    from irods import getFileUserMetadata, rcModAccessControl
    rev = model.repo.new_revision()
    conn = get_connection_from_params(params)
    resource = Resource.get(id)
    path = params['path']
    extras = {}
    # Lets handle only resources with file names
    if resource.name:
        fname = "%s/%s" % (path, resource.name.split('/')[-1])
        log.debug(fname)
        i = 0
        access = rcModAccessControl()
        log.debug(access.getPath())
        if conn:
            for met in getFileUserMetadata(conn, fname):
                i += 1
                key, value, _ = met
                extras[key] = value
            resource.extras = extras
            Session.add(resource)
            conn.disconnect()
            model.repo.commit()
            rev.message = "Update from iRODS, matched file %s" % fname
            h.flash_success("iRODS import to resource OK! Imported %s metadatas" % i)
        else:
            h.flash_error("Could not connect to iRODS!")
    else:
        h.flash_error("Resource is an URL, cannot import!")
    h.redirect_to(controller='package', action='resource_read', \
              id=resource.resource_group.package.name, \
              resource_id=resource.id)


class iRODSImport(BaseController):
    """
    Whole collection import to dataset as new resources in CKAN.
    """
    def view(self, id):
        """
        Render the import form, see if there is a POST request, then call
        import_irods_collection.
        """
        context = {'model':model, 'user': c.user or c.author}
        try:
            check_access('package_update', context, {'id' : id})
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))
        pkg = Package.get(id)
        c.pkg = pkg.name
        if ('save' in request.params):
            import_collection_to_package(request.params, id)
        return render('ckanext/irods/irods.html')


def import_collection_to_package(params, id):
    """
    Import a collection to dataset. Does not import whole file data but
    rather the metadata.
    """
    from irods import irodsCollection
    path = params['path']
    pkg = Package.get(id)
    conn = get_connection_from_params(params)
    if (conn):
        coll = irodsCollection(conn, path)
        from irods import iRodsOpen
        rev = model.repo.new_revision()
        i = 0
        for obj in coll.getObjects():
            extras = {} 
            fname, _ = obj
            fpath = "%s/%s" % (coll.getCollName(), fname) 
            f = iRodsOpen(conn, fpath, 'r')
            if f:
                i += 1
                res = Resource.by_name(fname)
                if not res:
                    res = Resource(url = '', name=fname, extras=extras, \
                                   resource_type='file')
                for met in f.getUserMetadata():
                    key, value, _ = met
                    extras[key] = value
                res.extras = extras
                resgrp = pkg.resource_groups[0]
                resgrp.resources.append(res)
                Session.add(res)
                Session.add(resgrp)
                rev.message = "Update from iRODS, matched file %s" % fname
        for met in coll.getUserMetadata():
            key, value, _ = met
            pkg.extras[key] = value
        Session.add(pkg)
        model.repo.commit()
        conn.disconnect()
        h.flash_success("iRODS import to dataset OK! Imported %s resources." % i)
    else:
        h.flash_error("Could not connect to iRODS!")
    h.redirect_to(controller='package', action='read', id=id)
