from horizon import views
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django import http
from django import shortcuts
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from horizon import tabs
from horizon.utils import memoized
from horizon import workflows

from openstack_dashboard import api
import urllib2
import json


from openstack_dashboard.dashboards.cmpe281billing.cmpe281billitemspanel \
import tables as project_tables

from openstack_dashboard.dashboards.cmpe281billing.cmpe281billitemspanel \
import tabs as project_tabs

class BillItem:
	def __init__(self,bill_item_id,desc,start_date,end_date,charge_amt,usage_amt,entity_name,currency):
	  self.id=bill_item_id
	  self.desc=desc
	  self.start_date=start_date
	  self.end_date=end_date
	  self.charge_amt=charge_amt
	  self.usage_amt=usage_amt
	  self.currency=currency
	  self.entity_name=entity_name


class IndexView(tables.DataTableView):
    table_class = project_tables.InstancesTable
    template_name = 'cmpe281billing/cmpe281billitemspanel/index.html'
    page_title = _("Bill Items")

    def get_data(self):
        #strobj = urllib2.urlopen('http://localhost:9000/billing/bill/'+self.request.user.tenant_id) 
        strobj = urllib2.urlopen('http://localhost:9000/billing/bill/f7ac731cc11f40efbc03a9f9e1d1d21f') 
        bills = json.load(strobj) 
        # Gather our instances
	ret = []
	for vbill in bills:
		for item in vbill['billing_item']:
		        ret.append(BillItem(item['bill_item_id'],
			   item['description'],
			   item['billing_period_start_time'],
			   item['billing_period_end_time'],
			   item['charge_amount'],
			   item['usage_amount'],
			   item['entity_name'],
			   'USD'
			   ))
		return ret


