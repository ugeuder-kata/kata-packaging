import logging
from mock import Mock
from pprint import pprint
from sqlalchemy import MetaData, __version__ as sqav
import ckan.model as model
from ckan.model import Package, Resource, meta, repo, Session
from ckan.lib.helpers import url_for,json

from ckan.tests import CreateTestData
from ckan.tests.functional.base import FunctionalTestCase

from ckanext.irods.controllers import iRODSView
from ckanext.irods.controllers import iRODSImport


log = logging.getLogger(__name__)

class TestRODS(FunctionalTestCase):

    @classmethod
    def setup_class(self):
        Session.remove()
        CreateTestData.create()

    @classmethod
    def teardown_class(self):
        Session.remove()

    def test_menuitem_for_package(self):
        name = 'annakarenina'
        offset = url_for(controller='package', action='read', id = name)
        res = self.app.get(offset)
        assert 'IRODS' in res

    def test_menuitem_for_resource(self):
        name = 'annakarenina'
        pkg = Package.by_name(name)
        res = pkg.resource_groups[0].resources[0]
        offset = url_for(controller='package', action='resource_read', id = name, resource_id = res.id)
        res = self.app.get(offset)
        assert 'IRODS' in res

    def test_resource_fetch(self):
        Session = Mock()
        getFileUserMetadata = Mock()
