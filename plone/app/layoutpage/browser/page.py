import os
from z3c.form import field
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from Products.Five import BrowserView
from plone.app.blocks.layoutbehavior import ILayoutAware
from plone.app.layoutpage.interfaces import IPage
from plone.dexterity.browser import add
from plone.app.dexterity.behaviors.metadata import IBasic


class PageView(BrowserView):
    
    @property
    def content(self):
        # make sure tiles will get rendered even without panel merging
        self.request['plone.app.blocks.merged'] = True
        
        return ILayoutAware(self.context).content


class PageAddForm(add.DefaultAddForm):
    additionalSchemata = ()
    
    fields = field.Fields(IBasic['title'])


class PageAddView(add.DefaultAddView):
    form = PageAddForm


pageLayoutFile = os.path.join(os.path.dirname(__file__), 'templates', 'page.html')
defaultPageLayout = open(pageLayoutFile).read()


@adapter(IPage, IObjectCreatedEvent)
def setDefaultLayoutForNewPage(obj, event):
    layoutAware = ILayoutAware(obj)
    layout = getattr(layoutAware, 'content', None)
    if layout is None:
        ILayoutAware(obj).content = defaultPageLayout
