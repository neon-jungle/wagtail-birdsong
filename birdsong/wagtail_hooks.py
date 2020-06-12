from wagtail.core.rich_text.pages import PageLinkHandler
from wagtail.core.rich_text import LinkHandler
from wagtail.core import hooks
from django.utils.html import escape

class AbsoluteLinkHandler(LinkHandler):
    identifier = 'page'
    @staticmethod
    def get_model():
        return Page

    @classmethod
    def get_instance(cls, attrs):
        return super().get_instance(attrs).specific

    @classmethod
    def expand_db_attributes(cls, attrs):
        print('expanding!')
        try:
            page = cls.get_instance(attrs)
            return f'<a href="Hooooo">'
        except Page.DoesNotExist:
            return "<a>"



@hooks.register('register_rich_text_features')
def register_absolute_link(features):
    print('here@@@')
    features.register_link_type(AbsoluteLinkHandler)
