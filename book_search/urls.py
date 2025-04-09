"""
URL configuration for book_search project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from book_data.views import (index, login_view, 
                            register, logout_view,
                            book_view, write_review, 
                            add_reading_list, user_reading_list,
                            remove_from_reading_list,
                            user_reviews_page, get_comment,
                            delete_comment, delete_review,
                            delete_review_from_list,
                            user_profile_page,
                            change_avatar)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register, name='register'),
    path("admin/", admin.site.urls),
    path('write-review/', write_review, name='write_review'),
    re_path(r'^add_reading_list/(?P<book_id>[^/]+)/(?P<cover_key>[^/]+)?/$', add_reading_list, name='add_reading_list'),
    path('change_avatar', change_avatar, name='change_avatar'),
    path('user_reviews_page/', user_reviews_page, name='user_reviews_page'),
    path('user_reading_list/', user_reading_list, name='user_reading_list'),
    path('get_comment/<int:review_id>', get_comment, name='get_comment'),
    path('delete_reviews_from_list/<int:review_id>', delete_review_from_list, name='delete_review_from_list'),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('delete_review/<int:review_id>', delete_review, name='delete_review'),
    path('remove/<str:book_id>', remove_from_reading_list, name='remove_from_reading_list'),
    path('user_profile_page/<int:user_id>', user_profile_page, name='user_profile_page'),
    re_path(r'^book_view/(?P<book_id>[^/]+)/(?P<cover_key>[^/]+)?/$', book_view, name='book_view')
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
