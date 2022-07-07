from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Room  , Student , Student_Group,CustomUser,Teacher,Student_check_count,Count_time


class UserModel(UserAdmin):
    fieldsets=(
        *UserAdmin.fieldsets,(
            'Type User',{
                'fields':(
                    'user_type',
                ),
            },
        ),
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','student_id','created')

class Student_GroupAdmin(admin.ModelAdmin):
    list_display = ('room_id','student_id')

class Student_check_countAdmin(admin.ModelAdmin):
    list_display = ('student_id','room_id','created')
     
class Count_timeAdmin(admin.ModelAdmin):
    list_display = ('studentid','count_time','codeset')

    def studentid(self,obj):
        return obj.code_set.student_id
    def codeset(self,obj):
        return obj.code_set.code_set

admin.site.register(CustomUser, UserModel)
admin.site.register(Teacher)
admin.site.register(Student,StudentAdmin)
admin.site.register(Student_Group,Student_GroupAdmin)
admin.site.register(Student_check_count,Student_check_countAdmin)
admin.site.register(Count_time,Count_timeAdmin)
admin.site.register(Room)
