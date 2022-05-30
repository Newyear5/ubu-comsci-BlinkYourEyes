from multiprocessing import context
from tkinter import Frame
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from .models import Room , CustomUser, Student_Group , Student
from .forms import RoomForm , RegisterForm ,StudentForm
from scipy.spatial import distance
from imutils import face_utils
import cv2
import dlib
import time
import imutils

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

def check_eye(vid_path):
    thresh = 0.25
    frame_check = 20
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("D:\\Drowsiness_Detection-master\\Drowsiness_Detection-master\\shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    time.sleep(1.0)
    flag=0
    check_round=0

    cap = cv2.VideoCapture(vid_path)

    if(cap.isOpened()== False):
        print("unable to read camera feed")

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("fps = " + str(fps))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('frame_count = '+ str(frame_count))
    duration = frame_count/fps
    print("Duration "+ str(duration) + ' seconds')
    minutes = int(duration/60)
    seconds = int(duration%60)
    print( str(minutes) +'.'+ str(seconds) + ' Min')
    start = last = count_time = duration_specific = 0
    w,h= 2, 100
    arr = [[0 for x in range(w)]for x in range(h)]

    while(cap.isOpened()):
    
        ret, frame = cap.read()
        if not ret:
            print("false")
            current_time_last = str(int((last/fps)/60))+"."+str(int((last/fps)%60))
            arr[count_time][duration_specific]=current_time_last
            for i in range(int(count_time+1)): 
                for j in range(2) :
                    print(arr[i][j],end=" ") 
            break
        frame = imutils.resize(frame, width=800,height=600)
        Frame_position = cap.get(cv2.CAP_PROP_POS_FRAMES)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
    
        # loop face
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
        
        # draw eye
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < thresh:
                flag += 1
			
                if flag >= frame_check:
                    #if detect will send data to array
                    if start == 0:
                        start = Frame_position
                        last = Frame_position
                        current_time_start = str(int((start/fps)/60))+"."+str(int((start/fps)%60))
                        arr[count_time][duration_specific]=current_time_start
                        duration_specific+=1
                    elif last-Frame_position == -1:
                        last = Frame_position
                    elif last-Frame_position != -1:
                        current_time_last = str(int((last/fps)/60))+"."+str(int((last/fps)%60))
                        arr[count_time][duration_specific]=current_time_last
                        count_time+=1
                        duration_specific = 0
                        start = Frame_position
                        last = Frame_position
                        current_time_start = str(int((start/fps)/60))+"."+str(int((start/fps)%60))
                        arr[count_time][duration_specific]=current_time_start
                        duration_specific+=1
                    
                    cv2.putText(frame, "****************ALERT!****************", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "****************ALERT!****************", (10,325),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				    #print ("Drowsy")
            else:
                flag = 0
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()        
    return count_time

def detect(request):
    if request.method =='POST' and request.FILES['myfile']:
        video_obj = request.FILES['myfile']
        cap = range(check_eye(video_obj.temporary_file_path()))
        print(cap)
    return redirect(request.META.get('HTTP_REFERER'))

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


    q = request.GET.get('q') if request.GET.get('q') != None else ''    
    rooms = Room.objects.filter(room_name__icontains=q)
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


    