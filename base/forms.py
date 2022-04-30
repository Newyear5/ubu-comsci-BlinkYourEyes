from django.forms import ModelForm, inlineformset_factory
from .models import Room, CustomUser,Student
from django import forms  
from django.core.exceptions import ValidationError

class RoomForm(ModelForm):
    queryset = CustomUser.objects.all()
    room_host = forms.ModelChoiceField(queryset=queryset,widget=forms.HiddenInput())
    class Meta:
        model = Room
        fields = ['room_host','room_name','room_id']



class StudentForm(ModelForm):
    student_id = forms.CharField(label='รหัสนักศึกษา',max_length=10)

    class Meta:
        model= Student
        exclude=('user',)  

class RegisterForm(ModelForm):
    user_choice=(
        ('1','student'),
        ('2','teacher'),
    )
    username = forms.CharField(label='Username',min_length=6,max_length=150)
    email = forms.EmailField(label='Email',max_length=254)
    password1 = forms.CharField(label='Password',min_length=6,widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    first_name = forms.CharField(label='ชื่อ',max_length=150)
    last_name = forms.CharField(label='นามสกุล',max_length=150)
    class Meta:
        model = CustomUser
        fields = ['username','password1','password2','first_name','last_name','email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



