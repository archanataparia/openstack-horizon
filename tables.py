# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging
import requests
from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponse  # noqa
from django import shortcuts
from django import template
from django.template.defaultfilters import title  # noqa
from django.utils.http import urlencode
from django.utils.translation import npgettext_lazy
from django.utils.translation import pgettext_lazy
from django.utils.translation import string_concat  # noqa
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import conf
from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.templatetags import sizeformat
from horizon.utils import filters

from openstack_dashboard import api
from openstack_dashboard import policy


LOG = logging.getLogger(__name__)

class UsePayment (policy.PolicyTargetMixin, tables.BatchAction):
    name = "Use Payment"
    classes = ('btn-confirm',)
    policy_rules = (("compute", "compute:start"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Use card",
            u"Used this card",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Bill Paid",
            u"Bills Paid",
            count
        )

    def allowed(self, request, instance):
        return 1

    def action(self, request, obj_id):
	url = "http://localhost:9000/billing/payment_method/"+request.user.tenant_id + "/"+ obj_id

class DelPayment (policy.PolicyTargetMixin, tables.BatchAction):
    name = "Delete Payment"
    classes = ('btn-confirm',)
    policy_rules = (("compute", "compute:start"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete card",
            u"Delete cards",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Card Deleted",
            u"Cards Deleted",
            count
        )

    def allowed(self, request, instance):
        return 1

    def action(self, request, obj_id):
	url = "http://localhost:9000/billing/payment_method/"+request.user.tenant_id + "/"+ obj_id
	requests.delete(url)



class LaunchLink(tables.LinkAction):
    name = "add_card"
    verbose_name = _("Add card")
    url = "horizon:cmpe281billing:cmpe281paymentmethodpanel:paybill"
    classes = ("ajax-modal", "btn-launch")
    icon = "cloud-upload"
    policy_rules = (("compute", "compute:create"),)
    ajax = True

    def __init__(self, attrs=None, **kwargs):
        kwargs['preempt'] = True
        super(LaunchLink, self).__init__(attrs, **kwargs)
    def allowed(self, request, datum):
        self.verbose_name = _("Add Card")
        #classes = [c for c in self.classes if c != "disabled"]
        #self.classes = classes
        return True  # The action should always be displayed

    def single(self, table, request, object_id=None):
        self.allowed(request, None)
        return HttpResponse(self.render())

CREDIT_CARD_TYPE_DISPLAY_CHOICES = (
    ("visa", pgettext_lazy("Visa credit card", u"Visa")),
    ("mastercard", pgettext_lazy("Mastercard credit card", u"Mastercard")),
)

class InstancesTable(tables.DataTable):
    CREDIT_CARD_TYPE_CHOICES = (
        ("visa", True),
        ("mastercard", True),
        ("saurabh", True),
    )
    card_num = tables.Column("card_num",
                         verbose_name=_("Card Number"))
#    name = tables.Column("Card holder Name",
#                         verbose_name=_("Card Holder Name"))
    type = tables.Column("type",
                       verbose_name=_("Card Type"))#,
#			status=True)#,
#			#status_choices=CREDIT_CARD_TYPE_CHOICES,
			#display_choices=CREDIT_CARD_TYPE_DISPLAY_CHOICES)
    vendor = tables.Column("vendor",
                       verbose_name=_("Card Vendor"))
    exp_month = tables.Column("exp_month",
                            verbose_name=_("Card Expiration Month")
                                     )
    exp_yr = tables.Column("exp_yr",
                            verbose_name=_("Card Expiration Year"))


    class Meta(object):
        name = "Payment Method"
        verbose_name = _("Payment Method")
        launch_actions = ()
        if getattr(settings, 'LAUNCH_INSTANCE_LEGACY_ENABLED', True):
            launch_actions = (LaunchLink,) + launch_actions
	table_actions = launch_actions
	row_actions = (UsePayment,DelPayment,)
