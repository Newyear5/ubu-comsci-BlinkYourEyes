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
    path('student-room/', views.studentRoom, name="student-room"),

    path('', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    path('student-group/', views.studentGroup, name="student-group"),
    path('student-room/', views.deleteGroup, name="delete-group"),
    path('student-room-group/<str:pk>/', views.studentRoomGroup, name="student-room-group"),
    

]