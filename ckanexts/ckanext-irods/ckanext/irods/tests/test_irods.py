"""
Tests for iRODS import and authorization.
"""
import logging
from ckan.model import Package, Session
from ckan.lib.helpers import url_for

from ckan.tests import CreateTestData
from ckan.tests.functional.base import FunctionalTestCase

log = logging.getLogger(__name__)

class TestRODS(FunctionalTestCase):
    """
    Quite simple test cases for iRODS import
    """
    @classmethod
    def setup_class(cls):
        """
        Remove any initial sessions.
        """
        Session.remove()
        # TODO: Should also remove test data
        CreateTestData.create()

    @classmethod
    def teardown_class(cls):
        """
        Tear down, remove the session.
        """
        Session.remove()

    def test_menuitem_for_package(self):
        """
        See if there is a 'IRODS' menuitem in the main menu for IRODS import,
        specifically for when a dataset is viewed.
        """
        name = 'annakarenina'
        offset = url_for(controller='package', action='read', id = name)
        res = self.app.get(offset)
        assert 'IRODS' in res

    def test_menuitem_for_resource(self):
        """
        See if there is a 'IRODS' menuitem in the main menu for IRODS import,
        specifically for when a resource is seen.
        """
        name = 'annakarenina'
        pkg = Package.by_name(name)
        res = pkg.resource_groups[0].resources[0]
        offset = url_for(controller='package', action='resource_read', \
                         id = name, resource_id = res.id)
        res = self.app.get(offset)
        assert 'IRODS' in res

    def test_resource_fetch(self):
        """
        A simple controller test for resource fetching from iRODS
        """
        name = 'annakarenina'
        pkg = Package.by_name(name)
        res = pkg.resource_groups[0].resources[0]
        result = self.app.get('/irods/'+res.id)
        form = result.forms['irods-form']
        form['server'] = 'irods.lan'
        form['uname'] = 'rods'
        form['pw'] = 'rods'
        form['port'] = '1247'
        form['zone'] = 'omaZone'
        form['path'] = '/omaZone/home/rods/ale.spec'
        formres = form.submit('save')
        assert not 'Could not' in formres

    def test_dataset_fetch(self):
        """
        A simple controller test for dataset fetching from iRODS
        """
        name = 'annakarenina'
        pkg = Package.by_name(name)
        result = self.app.get('/irods_import/'+pkg.id)
        form = result.forms['irods-form']
        form['server'] = 'irods.lan'
        form['uname'] = 'rods'
        form['pw'] = 'rods'
        form['port'] = '1247'
        form['zone'] = 'omaZone'
        form['path'] = '/omaZone/home/rods/ale.spec'
        formres = form.submit('save')
        assert not 'Could not' in formres
