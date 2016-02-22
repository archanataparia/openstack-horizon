from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.cmpe281billing import dashboard

class Cmpe281billitemspanel(horizon.Panel):
    name = _("Bill Items")
    slug = "cmpe281billitemspanel"


dashboard.Cmpe281billing.register(Cmpe281billitemspanel)
