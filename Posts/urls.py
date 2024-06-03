from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import post_list, post_details, register, add_post, edit_post, delete_post

urlpatterns = [
    path('posts/',post_list, name='post_list'),
    path('posts/post/<int:passed_id>/', post_details, name='detail_path'),
    # path('login/', user_login, name='login'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/register', register, name='register'),
    path('useraccount/add_post/', add_post, name='add_post'),
    path('useraccount/edit_post/<int:passed_id>/', edit_post, name='edit_post'),
    path('useraccount/delete_post/<int:passed_id>/', delete_post, name='delete_post')
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)