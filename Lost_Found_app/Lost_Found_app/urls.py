"""Lost_Found_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from graphene_django.views import GraphQLView 
from graphene_file_upload.django import FileUploadGraphQLView 
from django.conf.urls import url 


from databaseQueries.views import  EmpImageDisplay



urlpatterns = [
    path('admin/', admin.site.urls), 
    path('annIMG/<int:pk>/', EmpImageDisplay.as_view(), name='annoucement_img_display'),
    #path('graphql/', GraphQLView.as_view(graphiql=True)), 
    url(r'^graphql', FileUploadGraphQLView.as_view(graphiql=True)),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)