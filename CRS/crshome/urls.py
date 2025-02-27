from unicodedata import name
from django.urls import path
from .views import *
from crshome import views

app_name = 'home'

urlpatterns = [
        path('', views.Dashboard,name='dashboard'),
        path('login/', views.loginFunction,name='login'),
        path('reg/', views.Reg,name='reg'),
        path('police_reg/', views.Police_reg,name='policereg'),
        path('police_list/', views.Police_list,name='policelist'),
        path('userlist/', views.Userlist,name='userlist'),
        path('complaints/', views.ComplaintsList,name='complaints'),
        path('fir/', views.FirList,name='fir'),
        path('feedbacks/', views.FeedbackList,name='feedbacks'),
        path('delete-feedback/<int:id>/', views.DeleteFeedback,name='delete-feedback'),
        path('delete-fir/<int:id>/', views.DeleteFir,name='delete-fir'),
        path('delete-police/<int:id>/', views.DeletePolice,name='delete-police'),
        path('block-user/<int:id>/', views.BlockUser,name='block-user'),
        path('fir_reg/<int:id>/', views.Firreg,name='fir_reg'),
        path('add_fir', views.Addfir,name='add_fir'),
        path('fir_reject/<int:id>/', views.Firreject,name='fir_reject'),
        path('file-complaint/', views.FileComplaint,name='file-complaint'),
        path('create-feedback/', views.CreateFeedback,name='create-feedback'),
        path('logout/',logoutView,name='logout'),
        path('NoneuserFileComplaint/', views.NoneuserFileComplaint,name='NoneuserFileComplaint'),
        path('block_number/<str:num>/', views.blockNumber,name='block_number'),
        path('blocked/', views.BlockedList,name='blocked'),
        path('unblock-num/<int:id>/', views.UnblockNum,name='unblock-num'),
        path('mark-as-read/<int:id>/', views.MarkasRead,name='mark-as-read'),
        path('check-blocked/', views.CheckBlocked,name='check-blocked'),
        path('notifications/', views.Notifications,name='notifications'),
        path('check-email/', views.CheckEmail,name='check-email'),
        path('check-policeid/', views.CheckPoliceid,name='check-policeid'),
        path('solved-fir/<int:id>/', views.Solvedfir,name='solved-fir'),
        path('profile-edit/', views.ProfileEdit,name='profile-edit'),

]

