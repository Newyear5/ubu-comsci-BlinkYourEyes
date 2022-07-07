from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

import string,random


class CustomUser(AbstractUser):
    user_type = (('1','Student'),('2','Teacher'),('3','Admin'))
    user_type = models.CharField(default='1',choices=user_type, max_length=10)
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,verbose_name='username')
    student_id = models.CharField(max_length=100 , error_messages={'unique': 'A user with that student_id already exists.'},verbose_name='student_id',unique=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.student_id

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username

def number_string_random(size=6,chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Room(models.Model):
    room_host = models.ForeignKey(Teacher, on_delete = models.SET_NULL , null=True)
    room_name = models.CharField(max_length=70)
    room_id = models.CharField(max_length=10,unique=True,error_messages={'unique': 'Room_id already exists.'})
    group_code = models.CharField(max_length=6, default=number_string_random,unique=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.room_id

class Student_Group(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student , on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add = True)
     
    class Meta:
        ordering = ['-room_id']

    def __str__(self):
        return self.room_id.room_id

class Student_check_count(models.Model):
    student_id = models.ForeignKey(Student , on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room,on_delete=models.CASCADE)
    count_times = models.IntegerField()
    path_video = models.CharField(max_length=100)
    duration = models.CharField(max_length=20)
    date = models.CharField(max_length=50)
    code_set = models.CharField(max_length=10, default=number_string_random,unique=True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.student_id.student_id

class Count_time(models.Model):
    code_set = models.ForeignKey(Student_check_count, on_delete=models.CASCADE )
    count_time = models.IntegerField()
    start = models.CharField(max_length=10)
    stop = models.CharField(max_length=10)
    

    def __str__(self):
        return self.code_set.code_set


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       if instance.user_type == '2':
           Teacher.objects.create(user=instance)


