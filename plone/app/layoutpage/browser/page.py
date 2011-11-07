import os
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from Products.Five import BrowserView
from plone.app.blocks.layoutbehavior import ILayoutAware
from plone.app.layoutpage.interfaces import IPage


class PageView(BrowserView):
    
    @property
    def content(self):
        # make sure tiles will get rendered even without panel merging
        self.request['plone.app.blocks.merged'] = True
        
        return ILayoutAware(self.context).content


page_layout_file = os.path.join(os.path.dirname(__file__), 'templates', 'page.html')
default_page_layout = open(page_layout_file).read()

@adapter(IPage, IObjectCreatedEvent)
def setDefaultLayoutForNewPage(obj, event):
    ILayoutAware(obj).content = default_page_layout
