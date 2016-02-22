from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<ovs_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})/tables/(?P<db_name>.*)/(?P<table_name>.*)/$', views.ovsdb_table_data, name='ovsdb_table_data'),
    url(r'^(?P<ovs_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})/tables/(?P<db_name>.*)/$', views.ovsdb_table_list, name='ovsdb_table_list'),
    url(r'^(?P<ovs_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})/tables/$', views.ovsdb_list_dbs, name='ovsdb_list_dbs'),
]