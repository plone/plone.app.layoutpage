import os
import lxml
from urlparse import urljoin
from z3c.form import field
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from Products.Five import BrowserView
from plone.app.blocks.layoutbehavior import ILayoutAware
from plone.app.layoutpage.interfaces import IPage
from plone.dexterity.browser import add
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.blocks import utils

try:
    import json
    assert json
except:
    import simplejson as json


class PageView(BrowserView):

    @property
    def content(self):
        if getattr(self, '_content', None) is None:
            # make sure tiles will get rendered even without panel merging
            self.request['plone.app.blocks.merged'] = True
            self._content = ILayoutAware(self.context).content
        return self._content

    @property
    def tiles_instances(self):
        tiles = {}
        baseURL = self.request.getURL()
        tree = lxml.html.fromstring(self.content)

        for panelNode in utils.panelXPath(tree):
            panelName = panelNode.attrib['data-panel']

            for tileNode in utils.bodyTileXPath(panelNode):
                tileName = tileNode.attrib['data-tile']

                tileTree = utils.resolve(urljoin(baseURL, tileName))
                tile = tileTree.find('body')

                if panelName not in tiles.keys():
                    tiles[panelName] = {}

                tiles[panelName][tileName] = (tile.text or '') + \
                    ''.join([lxml.html.tostring(child) for child in tile])

        return json.dumps(tiles)


class PageAddForm(add.DefaultAddForm):
    additionalSchemata = ()

    fields = field.Fields(IBasic['title'])


class PageAddView(add.DefaultAddView):
    form = PageAddForm


pageLayoutFile = os.path.join(
    os.path.dirname(__file__), 'templates', 'page.html')
defaultPageLayout = open(pageLayoutFile).read()


@adapter(IPage, IObjectCreatedEvent)
def setDefaultLayoutForNewPage(obj, event):
    layoutAware = ILayoutAware(obj)
    layout = getattr(layoutAware, 'content', None)
    if layout is None:
        ILayoutAware(obj).content = defaultPageLayout
