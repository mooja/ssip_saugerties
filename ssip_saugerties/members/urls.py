from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.member_list,
        name='member_list'
    ),
    url(
        regex=r'^pdf/',
        view=views.member_list_pdf,
        name='member_list_pdf'
    ),
]
