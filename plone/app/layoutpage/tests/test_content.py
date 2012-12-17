# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.layoutpage.testing import LAYOUT_PAGE_INTEGRATION_TESTING
from plone.app.layoutpage.testing import LAYOUT_PAGE_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser


class IntegrationTests(unittest.TestCase):

    layer = LAYOUT_PAGE_INTEGRATION_TESTING

    def test_adding(self):

        # Ensure that invokeFactory() works as with normal types
        self.layer['folder'].invokeFactory('page', 'dp')

    def test_attributes_and_reindexing(self):
        from zope.lifecycleevent import modified

        # Demonstrate that dynamic types such as ``profilepage``
        # automatically get the attributes specified in their model, and
        # that content is reindexed when an IObjectModified event is fired.

        folder = self.layer['folder']
        folder.invokeFactory('page', 'dp', title='Old title')
        self.assertEquals('Old title', folder['dp'].title)

        folder['dp'].title = 'New Title'
        modified(folder['dp'])

        self.assertEquals('New Title', folder['dp'].title)

        results = self.layer['portal']['portal_catalog']({
            'Title': 'New title'})
        self.assertEquals(1, len(results))

    def test_layout_behavior_registered(self):
        from zope.component import getUtility
        from plone.behavior.interfaces import IBehavior
        from plone.app.blocks.layoutbehavior import ILayoutAware

        behavior = getUtility(
            IBehavior,
            name=u'plone.app.blocks.layoutbehavior.ILayoutAware')
        self.assertEqual(behavior.title, u'Layout support')
        self.assertEqual(behavior.interface, ILayoutAware)
        self.assertEqual(behavior.marker, ILayoutAware)

    def test_behavior_defaults(self):
        from plone.app.blocks.layoutbehavior import ILayoutAware

        self.layer['folder'].invokeFactory('page', 'dp')

        obj = self.layer['folder']['dp']
        layout = ILayoutAware(obj)

        from plone.app.layoutpage.browser.page import defaultPageLayout
        self.assertEqual(layout.content, defaultPageLayout)

    def test_behavior_default_page_layout(self):
        from plone.app.blocks.layoutbehavior import ILayoutAware

        self.layer['folder'].invokeFactory('page', 'dp')

        obj = self.layer['folder']['dp']

        layout = ILayoutAware(obj)

        from plone.app.layoutpage.browser.page import defaultPageLayout
        self.assertEqual(layout.content, defaultPageLayout)

    def test_page_schema(self):
        page = self.layer['portal'].portal_types.page
        self.assertEqual(page.schema, 'plone.app.layoutpage.interfaces.IPage')

    def test_is_folderish(self):
        ti = self.layer['portal'].portal_types.page
        self.assertEqual(ti.klass, 'plone.dexterity.content.Container')

        self.layer['folder'].invokeFactory('page', 'dp')
        page = self.layer['folder']['dp']

        # check we are allowed to create content inside the page - page itself
        # at least
        from zope.component import getMultiAdapter
        addable = getMultiAdapter((page, page.REQUEST),
                                  name='folder_factories').addable_types()
        self.assertTrue(len(addable) > 0)

        # check that invokeFactory works inside the page
        page.invokeFactory('page', 'subdp')
        subpage = self.layer['folder']['dp']['subdp']
        self.assertEqual(
            '/'.join(subpage.getPhysicalPath()), '/plone/foo-folder/dp/subdp')


class FunctionalTests(unittest.TestCase):

    layer = LAYOUT_PAGE_FUNCTIONAL_TESTING

    def test_add_extra_field_to_page_type(self):
        # ensure adding extra fields works as with normal types
        browser = Browser(self.layer['app'])
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME,
                          SITE_OWNER_PASSWORD))
        browser.open('http://nohost/plone/dexterity-types/page')
        browser.getControl('Add new field').click()
        browser.getControl('Title').value = 'Color'
        browser.getControl('Short Name').value = 'color'
        browser.getControl('Field type').value = ['Text line (String)']
        browser.getControl('Add').click()
        schema = self.layer['portal'].portal_types.page.lookupSchema()
        self.assertTrue('color' in schema.names())
        browser.open('http://nohost/plone/++add++page')
        # so we first add a new instances...
        browser.getControl(name='form.widgets.title').value = 'foo'
        browser.getControl(name='form.buttons.save').click()
        # ...which takes us directly to the edit form,
        # where the field should be present...
        browser.getControl(name='form.widgets.color').value = 'green'
        browser.getControl(name='form.buttons.save').click()
        foo = self.layer['portal']['foo']
        self.assertEqual(foo.portal_type, 'page')
        self.assertEqual(foo.color, 'green')
