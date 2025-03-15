from django.urls import path
from . import views
from django.conf import settings  # Import settings for media files
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('adminPage/',views.admin_page,name='adminPage'),
    path('addCourse/',views.add_course,name='addCourse'),
    path('updateCourse/',views.update_course,name='updateCourse'),
    path('properUpdateCourse/',views.proper_update,name='properUpdateCourse'),
    path('deleteCourse/',views.delete_course,name='deleteCourse'),
    path('courses/',views.courses,name='courses'),
    path('cartPage/',views.cart_page,name='cartPage'),
    path('middleCart/',views.middle_cart,name='middleCart'),
    path('search/',views.search,name='search'),
    path('profile/',views.profile,name='profile'),
    path('contact/',views.contact,name='contact'),
    path('buy/',views.buy,name='buy'),
    path('api/',views.apiCheck,name='api'),
    path("send_email/", views.send_email_to_user, name="send_email"),
    path('sendsms/',views.send_sms,name='sendsms'),
    path('chat/', views.chat_room, name='chat'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
