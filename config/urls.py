from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from account.views import Login, activate, signup
from payment.views import send_request, verify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comment/', include('comment.urls')),
    path("login/", Login.as_view(), name="login"),
    path("register/", signup, name="register"),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('', include('blog.urls')),
    path('', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('payment', include('payment.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
