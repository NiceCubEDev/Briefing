
from django.urls import path, include
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    # главная
    path('', MainView.showPage, name='main'),
    path('sendMessage/', MainView.mainSendMessage, name='post-message'),
    path('about_us/', MainView.mainAboutPage, name='about'),
    # path('chat/', chatbot_responseView, name='chat_response'), 
    path('contact/', MainView.mainContactPage, name="contact"), 


    #профиль
    path('account/profile/', ProfileView.showPage, name="profile"),
    path('account/profile/change/', ProfileView.changeData, name="profile-change_data"),
    path('account/profile/passed_inst/', ProfileView.passedBriefs, name="passed_brief_view"),
    path('account/profile/detail/', ProfileView.detail, name="profile_detail"),
    path('account/profile/action/', ProfileView.action, name="action"),
    path('account/profile/edit/', ProfileView.edit, name="profile_edit"),
    path('account/profile/passed_brief_filter/', ProfileView.sorting, name="passed_brief_filter_view"),
    

    #инструктажи
    path('account/themes_inst/test/<int:id>/checkFile/', BriefBrainView.checkFile, name = "check_down_load"),
    path('account/themes_inst/test/<int:id>/check/', BriefBrainView.checkPassed, name = "check_passed_view"),
    path('account/themes_inst/test/<int:id>/<int:num>/save', BriefBrainView.save, name = 'save_data_test'),
    path('account/themes_inst/test/<int:id>/<int:num>/data', BriefBrainView.questions, name = 'get_data_test'),
    path('account/themes_inst/', BriefLayoutView.listBriefs, name = "brief"),
    path('account/themes_inst/test/<int:id>/', BriefLayoutView.tests, name = "test_list"),
 
    # user urls
    path('account/themes_inst/test/<int:id>/<int:num>', testView, name = 'start_test'),
    
    path('account/journal/', journalView, name = "journal_view"),
    path('account/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('account/', include('django.contrib.auth.urls')),
]

# for images media ***** 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# ***


