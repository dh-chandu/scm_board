from django.urls import path
from django.conf.urls import url
from .views import home, branch_list_tags, branch_tags, list_branches
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^prdetails/(?P<pk>\d+)/$', branch_list_tags, name='branch_list_tags'),
    url(r'^prdetails/$', list_branches, name='list_branches'),
]