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

from openstack_dashboard.dashboards.cmpe281billing.cmpe281paymentmethodpanel \
import tables as project_tables

from openstack_dashboard.dashboards.cmpe281billing.cmpe281paymentmethodpanel \
    import workflows as project_workflows

class PaymentMethod:
	def __init__(self,id,identity,vendor,valid_thru,type,tenant_id):
	  self.id = id
	  self.card_num=identity
	  self.vendor=vendor.lower()
	  self.exp_month=valid_thru[0:2]
	  self.exp_yr=valid_thru[2:4]
	  self.type = type
	  self.tenant_id = tenant_id


class IndexView(tables.DataTableView):
    table_class = project_tables.InstancesTable
    template_name = 'cmpe281billing/cmpe281paymentmethodpanel/index.html'
    page_title = _("Payment Method")
    def get_data(self):
    #    strobj = urllib2.urlopen('http://localhost:9000/billing/payment_method/f7ac731cc11f40efbc03a9f9e1d1d21f') 
	print "tenant id is : " + self.request.user.tenant_id
	url = "http://localhost:9000/billing/payment_method/"+ self.request.user.tenant_id
        strobj = urllib2.urlopen(url) 
        payment_methods = json.load(strobj) 
        # Gather our instances
	ret = []

	for vpayment in payment_methods:
		ret.append(PaymentMethod(vpayment['payment_method_id'],
			   vpayment['identity'],
			   vpayment['vendor'],
			   vpayment['valid_through'],
			   vpayment['type'],
			   vpayment['tenant_id']
			   ))
	return ret



class PayBillView(workflows.WorkflowView):
    workflow_class = project_workflows.PayBill

    def get_initial(self):
        initial = super(PayBillView, self).get_initial()
        initial['project_id'] = self.request.user.tenant_id
        initial['user_id'] = self.request.user.id
        return initial

