from django.urls import path
from CC_app.views import*

urlpatterns = [
    
    path('',register_page,name='register_page'),
    path('login/',login_page,name='login_page'),
    path('dashboard/',dashboard_page,name='dashboard_page'),
    path('logout/',logout_page,name='logout_page'),
    path('profile/',profile_page,name='profile_page'),
    path('update-profile/',update_profile,name='update_profile'),
    path('calorie-list/',calorie_list,name='calorie_list'),
    path('add-calorie/',add_calorie,name='add_calorie'),
    path('update-calorie/<int:id>/',update_calorie,name='update_calorie'),
    path('delete-calorie/<int:id>/',delete_calorie,name='delete_calorie'),

    
]