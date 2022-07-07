from django.urls import path
from . import views


urlpatterns = [
    path('login/' and '', views.loginPage, name="login"),
    path('register/', views.register, name="register"),
    path('create-user', views.createuser, name="create-user"),
    path('logout/', views.logoutUser, name="logout"),
    path('admin-home/',views.adminhome , name = "admin-home"),

    path('teacher-home/',views.teacherhome , name = "teacher-home"),
    path('room/<str:pk>/',views.room , name = "room"),
    path('room/<str:pk>/liststudent',views.roomliststd , name = "list-student"),
    path('room/<str:pk>/listalert/<str:path_code>',views.roomlistalertstd , name = "list-alert"),
    path('create-room', views.createRoom, name="create-room"),
    path('delete-room/', views.deleteRoom, name="delete-room"),
    
    path('student-room/', views.studentRoom, name="student-room"),
    path('student-group/', views.studentGroup, name="student-group"),
    path('delete-group/', views.deleteGroup, name="delete-group"),
    path('student-in-room/<str:pk>/', views.studentinRoom, name="student-in-room"),
    path('student-room-record/<str:pk>/', views.studentroomrecord, name="student-room-record"),
    path('check-eye/', views.check_eye, name="check-eye"),
    path('detect-eye/<str:pk>', views.detect, name="detect-eye"),
    

]