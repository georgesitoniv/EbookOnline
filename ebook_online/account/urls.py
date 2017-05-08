from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^login/$', views.LogIn.as_view(), name="login"),
    url(r'^logout/$', views.LogOut.as_view(), name="logout"),
    url(r'^register/$', views.Register.as_view(), name="register"),
    url(r'^profile/(?P<slug>[-\w]+)/$', views.ProfileDetailView.as_view(), name="profile"),
    url(r'^edit-profile/(?P<slug>[-\w]+)/$', views.ProfileEditView.as_view(), name="edit_profile"),
    url(r'^change-password/(?P<slug>[-\w]+)/$', views.ChangePasswordView.as_view(), name="change_password"),
]