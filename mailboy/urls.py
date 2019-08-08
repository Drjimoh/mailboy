from django.contrib import admin
from django.urls import include, path
import mailinglist.urls 
import booker.urls 
import user.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user.urls, namespace='user')),
    path('mailinglist/', include(mailinglist.urls, 
    	namespace='mailinglist')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
]
