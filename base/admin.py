from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Room , Message , Student , Student_Group,CustomUser,Teacher


class UserModel(UserAdmin):
    fieldsets=(
        *UserAdmin.fieldsets,(
            'Custom Field Heading',{
                'fields':(
                    'user_type',
                ),
            },
        ),
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','student_id')

class Student_GroupAdmin(admin.ModelAdmin):
    list_display = ('room_id','student_id')

admin.site.register(CustomUser, UserModel)
admin.site.register(Teacher)
admin.site.register(Student,StudentAdmin)
admin.site.register(Student_Group,Student_GroupAdmin)
admin.site.register(Room)
admin.site.register(Message)