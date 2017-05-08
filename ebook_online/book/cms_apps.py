from django.utils.translation import ugettext as _

from cms.apphook_pool import apphook_pool
from cms.app_base import CMSApp

class BookApphook(CMSApp):
    app_name = "book"
    name = _("Book Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["book.urls"]

apphook_pool.register(BookApphook)