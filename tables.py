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

class InstancesFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('Bill id', _("Bill id"), True),
                      ('status', _("Status ="), True)
                      #('image', _("Image ID ="), True),
                      #('flavor', _("Flavor ID ="), True)
		     )


class InstancesTable(tables.DataTable):
    TASK_STATUS_CHOICES = (
        (None, True),
        ("none", True)
    )
    STATUS_CHOICES = (
        ("active", True),
        ("shutoff", True),
        ("suspended", True),
        ("paused", True),
        ("error", False),
        ("rescue", True),
        ("shelved", True),
        ("shelved_offloaded", True),
    )
    entity_name = tables.Column("entity_name",
                       verbose_name=_("Entity Name"))
    desc = tables.Column("desc",
                       verbose_name=_("Description"))
    start_date = tables.Column("start_date",
                            verbose_name=_("Charge Period Start Date"))
    end_date = tables.Column("end_date",
                            verbose_name=_("Charge Period End Date"))
    usage_amt = tables.Column("usage_amt",
                       verbose_name=_("Usage Amount"))
    charge_amt = tables.Column("charge_amt",
                       verbose_name=_("Charge Amount"))
    currency = tables.Column("currency",
                       verbose_name=_("Currency"))



    class Meta(object):
        name = "Bills"
        verbose_name = _("Bills")

