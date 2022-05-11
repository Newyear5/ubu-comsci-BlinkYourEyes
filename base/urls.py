from django.urls import path
from . import views


urlpatterns = [
    path('login/' and '', views.loginPage, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('home/',views.home , name = "home"),
    
    path('room/<str:pk>/',views.room , name = "room"),
    path('room/<str:pk>/liststudent',views.roomliststd , name = "list-student"),
    path('room/<str:pk>/listalert',views.roomlistalertstd , name = "list-alert"),
    path('', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    
    path('student-room/', views.studentRoom, name="student-room"),
    path('student-group/', views.studentGroup, name="student-group"),
    path('delete-group/', views.deleteGroup, name="delete-group"),
    path('student-in-room/<str:pk>/', views.studentinRoom, name="student-in-room"),
    path('student-room-record/<str:pk>/', views.studentroomrecord, name="student-room-record"),
    

]