from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.cmpe281billing import dashboard

class Cmpe281paymentmethodpanel(horizon.Panel):
    name = _("Payment Method")
    slug = "cmpe281paymentmethodpanel"


dashboard.Cmpe281billing.register(Cmpe281paymentmethodpanel)
