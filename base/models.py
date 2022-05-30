from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

import string,random


class CustomUser(AbstractUser):
    user_type = (('1','Student'),('2','Teacher'))
    user_type = models.CharField(default='1',choices=user_type, max_length=10)
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,verbose_name='username')
    student_id = models.CharField(max_length=100 , verbose_name='student_id',unique=True)
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
    room_host = models.ForeignKey(CustomUser, on_delete = models.SET_NULL , null=True)
    room_name = models.CharField(max_length=70)
    room_id = models.CharField(max_length=10,unique=True)
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

    def __str__(self):
        return self.room_id.room_id

class Student_check_count(models.Model):
    student_id = models.ForeignKey(Student , on_delete=models.CASCADE)
    

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete= models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body[0:50]

#@receiver(post_save,sender=CustomUser)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        if instance.user_type == '1':
#            Student.objects.create(user=instance)
#       if instance.user_type == '2':
#           Teacher.objects.create(user=instance)


