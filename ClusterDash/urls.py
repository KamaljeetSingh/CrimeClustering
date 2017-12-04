from django.conf.urls import url, include
from . import views
app_name = 'cluster'

urlpatterns = [

    url(r"^$", views.cluster_home , name='cluster_home'),

]