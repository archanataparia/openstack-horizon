from django.utils.translation import ugettext_lazy as _

import horizon

class Cmpe281BillingGroup(horizon.PanelGroup):
    slug = "BillingGroup"
    name = _("BillingGroup")
    panels = ('cmpe281paymentpanel',
              'cmpe281billitemspanel',
              'cmpe281paymentmethodpanel',)


class Cmpe281billing(horizon.Dashboard):
    name = _("CMPE281_billing")
    slug = "cmpe281billing"
    panels = (Cmpe281BillingGroup,)  # Add your panels here.
    default_panel = 'cmpe281paymentpanel'  # Specify the slug of the dashboard's default panel.


horizon.register(Cmpe281billing)
