from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from datetime import datetime
from .models import  Room , Student_Group , Student, Student_check_count , Count_time, Teacher
from .forms import RoomForm , RegisterForm ,StudentForm , RegisterTeacherForm
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
    predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    time.sleep(1.0)
    flag=0
    cap = cv2.VideoCapture(vid_path)

    if(cap.isOpened()== False):
        print("unable to read camera feed")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    minutes = int(duration/60)
    seconds = int(duration%60)
    duration_time = str(minutes)+"."+str(seconds)
    print("fps = " + str(fps))
    print('frame_count = '+ str(frame_count))
    print("Duration "+ str(duration) + ' seconds')
    print( duration_time + ' Min')
    start = last = count_time = count_time_chk = duration_specific = 0
    finish = ""
    w,h= 2, 100
    arr = [[0 for x in range(w)]for x in range(h)]

    while(cap.isOpened()):
    
        ret, frame = cap.read()

        if not ret:
            print("finish checking")
            finish = "finish checking"
            if count_time_chk > 0:
                current_time_last = str(int((last/fps)/60))+"."+str(int((last/fps)%60))
                arr[count_time][duration_specific]=current_time_last
                break
            else:
                print("undetectable sleep")

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
                        count_time_chk+=1
                        start = Frame_position
                        last = Frame_position
                        current_time_start = str(int((start/fps)/60))+"."+str(int((start/fps)%60))
                        arr[count_time][duration_specific]=current_time_start
                        duration_specific+=1
                    #check if still asleep.
                    elif last-Frame_position == -1:
                        last = Frame_position
                    #check if still asleep another
                    elif last-Frame_position != -1:
                        current_time_last = str(int((last/fps)/60))+"."+str(int((last/fps)%60))
                        arr[count_time][duration_specific]=current_time_last
                        count_time+=1
                        count_time_chk+=1
                        duration_specific = 0
                        start = Frame_position
                        last = Frame_position
                        current_time_start = str(int((start/fps)/60))+"."+str(int((start/fps)%60))
                        arr[count_time][duration_specific]=current_time_start
                        duration_specific+=1
                    #show Alert message
                    cv2.putText(frame, "****************ALERT!****************", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "****************ALERT!****************", (10,325),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				    
            else:
                flag = 0
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()        
    return count_time_chk,arr,duration_time

def detect(request,pk):
    student = Student.objects.get(user=request.user)
    room = Room.objects.get(room_id=pk)
    if request.method =='POST' and request.FILES['myfile']:
        now = datetime.now()
        datenow = now.strftime("%d/%b/%Y")
        timenow = now.strftime("%X")
        date_time = "วันที่ "+datenow+" เวลา "+timenow
        video_obj = request.FILES['myfile']
        video_path = video_obj.temporary_file_path()
        count,video_set,durations = check_eye(video_path)
        #if undetectable sleep
        if count == 0:
            check_count = Student_check_count(
                student_id=student,
                room_id=room,
                count_times=count,
                path_video=video_path,
                duration=durations,
                date = date_time ,
            )
            check_count.save()
            messages.success(request, 'Form submission successful')
        #if detect sleep
        else :
            check_count = Student_check_count(
                student_id=student,
                room_id=room,
                count_times=count,
                path_video=video_path,
                duration=durations,
                date = date_time ,
            )
            check_count.save()
            for i in range(count):
                start=video_set[i][0]
                stop=video_set[i][1]
                count_times = Count_time(
                    code_set = check_count,
                    count_time = i ,
                    start = start,
                    stop = stop
                )
                count_times.save()
            messages.success(request, 'Form submission successful')
    return redirect(request.META.get('HTTP_REFERER'))

def loginPage(request):
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
                return redirect('teacher-home')  
            else :
                return redirect('admin-home')  
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
            messages.warning(request,'รหัสนักศึกษานี้ถูกใช้แล้ว')
    else:
        re_form = RegisterForm()
        student_form = StudentForm()

    context={'re_form' : re_form ,'student_form': student_form}
    return render(request ,'base/register.html',context)

def createuser(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    if request.method == 'POST' :
        teacherform = RegisterTeacherForm(request.POST)
        if teacherform.is_valid():
            teacherform.save()
            messages.success(request, 'Form submission successful')
            return redirect('admin-home')
        else:
            messages.warning(request,'Username already exist')

    return redirect(request.META.get('HTTP_REFERER'))

def logoutUser(request):
    logout(request)
    return redirect('login')

def adminhome(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

   
    rooms = Room.objects.all()
    students = Student.objects.all().order_by('student_id')
    teachers = Teacher.objects.all()
    formuser = RegisterTeacherForm()
    room_count = rooms.count()
    student_count = students.count()
    teacher_count = teachers.count()

    context = {'rooms': rooms ,
    'students':students,
    'teachers':teachers, 
    'student_count':student_count,
    'teacher_count':teacher_count,
    'room_count':room_count , 
    'formuser':formuser,
    }
    return render(request,'base/admin_home.html' , context)

def teacherhome(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')


    q = request.GET.get('q') if request.GET.get('q') != None else ''
    teacher = Teacher.objects.get(user=request.user)
    rooms = Room.objects.filter(room_name__icontains=q,room_host=teacher)
    form = RoomForm(initial={'room_host':teacher})
    formuser = RegisterTeacherForm()
    room_count = rooms.count()

    context = {'rooms': rooms , 
    'room_count':room_count , 
    'form':form,
    'formuser':formuser,
    }
    return render(request,'base/teacher_home.html' , context)


def room(request, pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    room = Room.objects.get(room_id=pk)
    list_students_alert = Student_check_count.objects.filter(room_id=room)
    

    context = {'room' : room,
     'list_students_alert':list_students_alert,
     }
    return render(request, 'base/room.html',context)

def studentRoom(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(room_name__icontains=q)
    students = Student.objects.get(user=request.user)
    groups = Student_Group.objects.filter(student_id=students,room_id__in=Room.objects.filter(room_name__icontains=q))


    context = {'students':students ,'groups':groups ,'rooms':rooms}
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
        st_groupcode = request.POST['group_code']
        room = Room.objects.filter(group_code=st_groupcode).first()
        if room is not None:
            if not Student_Group.objects.filter(room_id=room,student_id=student).exists():
                st_group = Student_Group(room_id=room,student_id=student)
                st_group.save()
                messages.success(request, 'Join Success')
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
    students = Student.objects.get(user=request.user)
    rooms = Room.objects.get(room_id=rid)

    if request.method == 'POST' :
        delst_group = Student_Group.objects.get(room_id=rooms,student_id=students)
        delst_group.delete()
        messages.success(request, 'Quit Success')
        return redirect('student-room')
        
    return redirect(request.META.get('HTTP_REFERER'))


def createRoom(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    if request.method == 'POST' :
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Create Success')
            return redirect('teacher-home')
        else:
            messages.warning(request,'Room_id is already exists')

    return redirect(request.META.get('HTTP_REFERER'))

def deleteRoom(request):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')
    
    rid = request.POST['room_id']
    room = Room.objects.get(room_id=rid)

    if request.method == 'POST' :
        room.delete()
        messages.success(request, 'Delete Success')
        return redirect('teacher-home')

    return redirect(request.META.get('HTTP_REFERER'))

def roomliststd(request,pk):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    
    room = Room.objects.get(room_id=pk)
    groups_st = Student_Group.objects.filter(room_id=room).order_by('student_id')
    groups_count = groups_st.count()
    
    context = {'room' : room,
     'groups_st': groups_st ,
     'groups_count' : groups_count,
     }
    return render(request, 'base/room_liststudent.html',context)

def roomlistalertstd(request,pk,path_code):
    if not request.user.is_authenticated:
        return render(request,'base/login_error.html')

    room = Room.objects.get(room_id=pk)
    student_count = Student_check_count.objects.get(code_set=path_code)
    count_set = Count_time.objects.filter(code_set=student_count)
   
    context = {'room' : room,
    'student_count':student_count,
    'count_set':count_set,
     }
    return render(request, 'base/room_listalertstudent.html',context)


    