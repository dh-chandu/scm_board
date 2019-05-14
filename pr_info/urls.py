from django.urls import path
from django.conf.urls import url
from .views import  info_branch_list_tags, info_list_branches
urlpatterns = [
    url(r'^prinfo/(?P<pk>\d+)/$', info_branch_list_tags, name='info_branch_list_tags'),
    url(r'^prinfo/$', info_list_branches, name='info_list_branches'),
]