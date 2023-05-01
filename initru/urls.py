
from django.urls import path, include
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # главная
    path('', mainView.mainPage, name='main'),
    path('sendMessage/', mainView.mainSendMessage, name='post-message'),
    path('about_us/', mainView.mainAboutPage, name='about'),
    path('chat/', chatbot_responseView, name='chat_response'), 
    path('contact/', mainView.mainContactPage, name="contact"), 

    #профиль
    path('account/profile/', profileView.mainPage, name="profile"),
    path('account/profile/change/', profileView.changeData, name="profile-change_data"),
    path('account/profile/passed_inst/', profileView.passedBriefs, name="passed_brief_view"),
    path('account/profile/detail/', profileView.detail, name="profile_detail"),
    path('account/profile/action/', profileView.action, name="action"),
    path('account/profile/edit/', profileView.edit, name="profile_edit"),
    path('account/profile/passed_brief_filter/', profileView.sorting, name="passed_brief_filter_view"),
    

    # user urls
    path('account/themes_inst/test/<int:id>/<int:num>/save', testDataSaveView, name = 'save_data_test'),
    path('account/themes_inst/test/<int:id>/<int:num>/data', testDataView, name = 'get_data_test'),
    path('account/themes_inst/test/<int:id>/<int:num>', testView, name = 'start_test'),
    path('account/themes_inst/test/<int:id>/check/', checkPassedView, name = "check_passed_view"),
    path('account/themes_inst/test/<int:id>/checkFile/', checkFileDownloadedView, name = "check_down_load"),
    path('account/themes_inst/test/<int:id>/', testsPageView, name = "test_list"),
    path('account/themes_inst/', briefPageView, name = "brief"),
    path('account/journal/', journalView, name = "journal_view"),
   


    
    path('account/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('account/', include('django.contrib.auth.urls')),
]

# for images media ***** 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# ***


