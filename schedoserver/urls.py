"""
URL configuration for schedoserver project.

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
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse


# Create a simple view that returns the CSRF token as JSON
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrftoken': token})

# View to return "Hello World" for root URL
def hello_world(request):
    return HttpResponse("Hello World")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-csrf-token/', get_csrf_token),
    path('accounts/', include('apps.accounts.urls')),
    path('events/', include('apps.events.urls')),
    path('registrations/', include('apps.registrations.urls')),
    # path('notifications/', include('apps.notifications.urls')),
    path('', hello_world),
]
