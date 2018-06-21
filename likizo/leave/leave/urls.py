"""leave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from leave_app import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^list_leaves$', views.list_leave, name='list_leave'),
    # valid url /leave/evodia/
    # capture {'username':'evodia'}

    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),


    url(r'^reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
        email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt'),
        name='password_reset'),

    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    url(r'^settings/password/$',
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),

    url(r'^settings/password/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),


    url(r'^users/list/$', accounts_views.UserListView.as_view(), name='list_users'),
    url(r'^users/update/(?P<user_id>\d+)/$', accounts_views.UserUpdateView.as_view(), name='update_users'),
    url(r'^users/delete/(?P<user_id>\d+)/$', accounts_views.DeleteUserView.as_view(), name='delete_users'),



    url(r'^leave/profile/(?P<username>[\w.@+-]+)/$', views.list_user_leave, name='list_user_leave'),
    url(r'^leave/new/$', views.new_leave, name='new_leave'),
    url(r'^leave/update/(?P<leave_id>\d+)/$', views.edit_leave, name='edit_leave'),
    url(r'^leave/delete/(?P<leave_id>\d+)/$', views.DeleteLeaveView.as_view(), name='delete_leave'),


    url(r'^department/(?P<leave_id>\d+)/leaves/$', views.AllNewLeavesByDepartmentList.as_view(), name='department_leaves'),




    url(r'^approve/leave/(?P<leave_id>\d+)/supervisor/$',
        views.LeaveApprovedBySupervisor.as_view(), name='supervisor_approve'),
    # valid url /approve/leave/leave_id/supervisor/
    url(r'^approve/leave/(?P<leave_id>\d+)/controller/$',
        views.LeaveApprovedByManager.as_view(), name='manager_approve'),
    # valid url /approve/leave/leave_id/controller/
    url(r'^admin/', admin.site.urls),
]
