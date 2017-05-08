from django.utils.translation import ugettext as _

from cms.apphook_pool import apphook_pool
from cms.app_base import CMSApp

class AccountApphook(CMSApp):
    app_name = "account"
    name = _("Account Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["account.urls"]

apphook_pool.register(AccountApphook)