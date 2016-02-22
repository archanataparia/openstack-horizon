from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.cmpe281billing.cmpe281paymentmethodpanel import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^paybill$', views.PayBillView.as_view(), name='paybill'),
)
