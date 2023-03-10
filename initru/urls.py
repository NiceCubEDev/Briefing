
from django.urls import path, include
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # guest urls
    path('', mainView, name='main'),
    path('about_us/', aboutPageView, name='about'),
    path('contact/', contactPageView, name="contact"),
    # admin urls
    path('createUser/', createUserAdmin, name ='user_create'),

    # user urls
    path('account/themes_inst/test/<int:id>/<int:num>/save', testDataSaveView, name = 'save_data_test'),
    path('account/themes_inst/test/<int:id>/<int:num>/data', testDataView, name = 'get_data_test'),
    path('account/themes_inst/test/<int:id>/<int:num>', testView, name = 'start_test'),
    path('account/themes_inst/test/<int:id>/', testsPageView, name = "test_list"),
    path('account/themes_inst/', briefPageView, name = "brief"),
    path('account/profile/', profileView, name="profile"),
    path('account/profile/detail/', getDetailProfile, name="profile_detail"),
    path('account/profile/edit/', getEditProfile, name="profile_edit"),
    path('account/profile/passed_inst/', passedView, name="profile_edit"),
    path('account/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('account/', include('django.contrib.auth.urls')),
]

# for images media ***** 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# ***


