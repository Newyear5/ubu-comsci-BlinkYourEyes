from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from .models import Room , CustomUser, Student_Group , Student
from .forms import RoomForm , RegisterForm ,StudentForm




def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username , password= password)

        if user is not None :
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('student-room')
            elif user_type == '2':
                return redirect('home')  
        else :
            messages.error(request,'Username or Password incorrect')


    context={}
    return render(request, 'base/login.html', context)

def register(request):
    if request.method == 'POST' :
        re_form = RegisterForm(request.POST)
        student_form = StudentForm(request.POST)
        if re_form.is_valid() and student_form.is_valid():
            form = re_form.save()
            student = student_form.save(commit=False)
            student.user = form
            student.save()
            student_form.save()
            messages.success(request, 'Form submission successful')
            return redirect('login')
        else:
            messages.warning(request,'Please correct the errors below')
    else:
        re_form = RegisterForm()
        student_form = StudentForm()

    context={'re_form' : re_form ,'student_form': student_form}
    return render(request ,'base/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')


    q = request.GET.get('q')
    if q is not None:
        rooms = Room.objects.filter(room_name__icontains=q)
    else:
        q = ''
    users = CustomUser.objects.filter()
    form = RoomForm(initial={'room_host':request.user})
    room_count = rooms.count()
    user_count = users.count()

    context = {'rooms': rooms , 
    'room_count':room_count , 
    'user_count':user_count,
    'form':form,
    }
    return render(request,'base/home.html' , context)


def room(request, pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    
    room = Room.objects.get(room_id=pk)
    groups_st = Student_Group.objects.filter(room_id=room)
    student = Student.objects.all()
    groups_count = groups_st.count()
    room_messages = room.message_set.all().order_by('-created')
    context = {'room' : room,
     'student' : student ,
     'groups_st': groups_st ,
     'room_messages' : room_messages,
     'groups_count' : groups_count,
     }
    return render(request, 'base/room.html',context)

def studentRoom(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(room_name__icontains=q)
    students = Student.objects.get(user=request.user)
    groups = Student_Group.objects.filter(student_id=students)

    group_count = groups.count()


    context = {'students':students ,'groups':groups ,'group_count':group_count ,'rooms':rooms}
    return render(request,'base/Student_room.html',context)


def studentinRoom(request,pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')
    

    students = Student.objects.get(user=request.user)
    rooms = Room.objects.get(room_id=pk)

    context = {'students':students ,'rooms':rooms}
    return render(request,'base/student_in_room.html',context)

def studentroomrecord(request,pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    students = Student.objects.get(user=request.user)
    groups = Student_Group.objects.filter(student_id=students)
    rooms = Room.objects.get(room_id=pk)  

    context = {'students':students,'groups':groups ,'rooms': rooms}
    return render(request,'base/student_room_record.html',context)

def studentGroup(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        st_groupcode = request.POST['groupcode']
        room = Room.objects.get(group_code=st_groupcode)
        if room is not None:
            if not Student_Group.objects.filter(room_id=room,student_id=student).exists():
                st_group = Student_Group(room_id=room,student_id=student)
                st_group.save()
                return redirect('student-room')
            else:
                messages.warning(request,'Already Joined')  
        else :
            messages.warning(request,'group_code invalid')
    
    return redirect(request.META.get('HTTP_REFERER'))

def deleteGroup(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')
    
    rid = request.POST['group_id']
    delst_group = Student_Group.objects.get(room_id=rid)
    if request.method == 'POST' :
        delst_group.delete()
        return redirect('student-room')
        
    return redirect(request.META.get('HTTP_REFERER'))


def createRoom(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    form = RoomForm()
    if request.method == 'POST' :
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return redirect(request.META.get('HTTP_REFERER'))


def updateRoom(request, pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    room = Room.objects.get(room_id=pk)
    form = RoomForm(instance=room)

    if request.user != room.room_host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)    


def deleteRoom(request, pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')
    

    room = Room.objects.get(room_id=pk)
    if request.method == 'POST' :
        room.delete()
        return redirect('home')

    context = {'room': room}
    return render(request, 'base/delete.html', context )

def roomliststd(request,pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    
    room = Room.objects.get(room_id=pk)
    groups_st = Student_Group.objects.filter(room_id=room)
    student = Student.objects.all()
    groups_count = groups_st.count()
    
    context = {'room' : room,
     'student' : student ,
     'groups_st': groups_st ,
     'groups_count' : groups_count,
     }
    return render(request, 'base/room_liststudent.html',context)

def roomlistalertstd(request,pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    
    room = Room.objects.get(room_id=pk)
    groups_st = Student_Group.objects.filter(room_id=room)
    student = Student.objects.all()
   
    context = {'room' : room,
     'student' : student ,
     'groups_st': groups_st ,

     }
    return render(request, 'base/room_listalertstudent.html',context)


    