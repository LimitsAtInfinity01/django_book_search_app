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

from django.contrib import admin
from django.urls import path
from book_data.views import (index, login_view, 
                            register, logout_view,
                            book_view, write_review, 
                            add_reading_list, user_reading_list)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register, name='register'),
    path("admin/", admin.site.urls),
    path('write-review/', write_review, name='write_review'),
    path('add_reading_list/', add_reading_list, name='add_reading_list'),
    path('user_reading_list/', user_reading_list, name='user_reading_list'),
    path('book_view/<str:book_id>/<str:cover_key>/', book_view, name='book_view')
]
