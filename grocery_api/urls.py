from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Add this line
]


## visits: http://localhost:8000/api/products/

##1. Django checks grocery_api/urls.py
##   → Finds path('api/', ...) → strips 'api/' 
   
##. Remaining: 'products/' goes to api/urls.py
 #  → Router matches 'products/' to ProductViewSet
   
## ProductViewSet.list() executes → returns all products

