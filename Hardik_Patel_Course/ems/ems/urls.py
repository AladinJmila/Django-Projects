from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/', include('employee.urls')),
    path('polls/', include('poll.urls')),
    path('api/v1/', include('employee.api_urls'))
]
