import datetime
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from ksd import exracttext
from lk import veidosumma
from .models import *

# Create your views here.

def log(request):
    return render(request,"login_index.html")


def login_post(request):
    username1 =request.POST['textfield']
    password1 =request.POST['textfield2']
    lobj = login.objects.filter(username=username1,password=password1)
    if lobj.exists():
        lobj = lobj[0]
        request.session['lid'] = lobj.id
        print("AAA",request.session['lid'])
        if lobj.usertype == 'admin':
            return HttpResponse("<script>alert('welcome ');window.location='/admin_home'</script>")

        if lobj.usertype == 'parent':
            request.session['pid']=parent.objects.get(LOGIN_id=lobj.id).id
            return HttpResponse("<script>alert('welcome ');window.location='/daycare_home'</script>")
        if lobj.usertype == 'staff':
            request.session['sid']=staff.objects.get(LOGIN_id=lobj.id).id
            return HttpResponse("<script>alert('welcome ');window.location='/staff_home'</script>")
        if lobj.usertype == 'teacher':
            # request.session['lid'] = lobj.id
            request.session['tid'] = teacher.objects.get(LOGIN=request.session['lid']).id
            return HttpResponse("<script>alert('welcome ');window.location='/teacher_home'</script>")
        else:
            return HttpResponse("<script>alert('Not found ');window.location='/'</script>")
    return HttpResponse("<script>alert('User not found');window.location='/'</script>")


def change_password(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request,"admin/change password.html")


def change_password_post(request):
    Current_password=request.POST['textfield']
    New_password=request.POST['textfield2']
    Confirm_password=request.POST['textfield2']
    data = login.objects.filter(id=request.session['lid'],password=Current_password)
    if data.exists():
        if New_password == Confirm_password:
            login.objects.filter(id=request.session['lid']).update(password=Confirm_password)
            return HttpResponse("<script>alert('Success');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('Failed');window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('Not Found');window.location='/'</script>")

def send_reply(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")




    return render(request,"admin/send reply.html",{"id":id})

def send_reply_post(request,id):
    reply=request.POST['textfield3']
    import datetime
    date=datetime.datetime.now()
    complaint.objects.filter(id=id).update(reply=reply,reply_date=date)
    return HttpResponse("<script>alert('Reply sent successfully');window.location='/view_complaint#aa'</script>")

def send_replyy(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")



    return render(request,"staff/send reply.html",{"id":id})

def send_replyy_post(request,id):
    reply=request.POST['textfield3']
    import datetime
    date=datetime.datetime.now()
    Enquiry.objects.filter(id=id).update(reply=reply,reply_date=date)
    return HttpResponse("<script>alert('Reply sent successfully');window.location='/view_enquiry#aa'</script>")

def verified_daycare(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")


    data=daycare.objects.filter(LOGIN__usertype='daycare')
    return render(request,"admin/verified day care.html",{'view':data})

def view_and_verify_daycare(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")


    data=daycare.objects.filter(LOGIN__usertype='pending')
    return render(request,"admin/view and verify daycare.html",{'day':data})

def approve(request,id):

    login.objects.filter(id=id).update(usertype="daycare")
    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("jasijaseer06@gmail.com", "wkxf jffn jsda qogm")
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = "jasijaseer06@gmail.com"
    msg['To'] = login.objects.filter(id=id)[0].username
    msg['Subject'] = "Your request for daycare registration in approved"
    body = "VERIFICATION"
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return HttpResponse("<script>alert('Approved');window.location='/verified_daycare'</script>")


def reject(request,id):
    login.objects.filter(id=id).update(usertype="rejected")
    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("jasijaseer06@gmail.com", "wkxf jffn jsda qogm")
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = "jasijaseer06@gmail.com"
    msg['To'] = login.objects.filter(id=id)[0].username
    msg['Subject'] = "Your request for daycare registration is rejected"
    body = "VERIFICATION"
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return HttpResponse("<script>alert('Rejected');window.location='/view_and_verify_daycare'</script>")


def view_complaint(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = complaint.objects.all()
    return render(request,"admin/view complaint.html",{'comp':data})

def view_feedback(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = feedback.objects.all()
    return render(request,"admin/view feedback.html",{'feed':data})

def view_rating(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = rating.objects.all()
    return render(request,"admin/view rating.html",{'rat':data})

def view_student(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data=student.objects.all()
    return render(request,"admin/view student.html",{'stu':data})

def view_teacher_in_daycare(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data=teacher.objects.filter(DAYCARE_id=id)
    return render(request,"admin/view teacher in  daycare.html",{'teach':data})

def admin_home(request):
    return  render(request,'admin/admin_index.html')


#------------------------ daycare =----------

def add_facility(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/add_facility.html')

def add_facility_post(request):
    fac=request.POST['textfield']
    description=request.POST['textarea']
    data = daycare_facility.objects.filter(facility=fac,DAYCARE=request.session['did'])

    if data.exists():
        return HttpResponse("<script>alert('facility already added');window.location='/view_facility#aa'</script>")
    else:

        obj=daycare_facility()
        obj.facility=fac
        obj.description=description
        obj.DAYCARE_id = request.session['did']
        obj.save()


        return HttpResponse("<script>alert('successs');window.location='/view_facility'</script>")



def add_fee(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/add_fee.html')

def add_fee_post(request):
    fees=request.POST['textfield']
    Age_group=request.POST['select']
    data = fee.objects.filter(age_group=Age_group, DAYCARE = request.session['did'])

    if data.exists():
        return HttpResponse("<script>alert('fee already added');window.location='/view_fee'</script>")
    else:
        obj=fee()
        obj.fee1=fees
        obj.age_group=Age_group
        obj.DAYCARE_id = request.session['did']
        obj.save()
        return HttpResponse("<script>alert('successs');window.location='/view_fee#aa'</script>")
def view_fee(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = fee.objects.filter(DAYCARE=request.session['did'])
    return render(request, 'Daycare/view_fee.html', {'cee': data})






def add_food_menu(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/add_food_menu.html')

def add_food_menu_post(request):
    day=request.POST['select2']
    food=request.POST['textfield2']
    info=request.POST['select']

    data = food_menu.objects.filter(food=food,day=day, DAYCARE=request.session['did'])

    if data.exists():
        return HttpResponse("<script>alert('food menu already added');window.location='/view_food_menu_new#aa'</script>")
    else:
        obj=food_menu()
        obj.food=food

        obj.info=info
        obj.day=day
        obj.DAYCARE_id = request.session['did']
        obj.save()

        return HttpResponse("<script>alert('successs');window.location='/view_food_menu_new#aa'</script>")

def add_meeting(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/add_meeting.html')

def add_meeting_post(request):
    date=request.POST['textfield']
    time=request.POST['textfield2']
    decription=request.POST['textarea']

    data = meeting.objects.filter(time=time, DAYCARE = request.session['did'])

    if data.exists():
        return HttpResponse("<script>alert('meeting already added');window.location='/add_meeting#aa'</script>")
    else:
        obj = meeting()
        obj.date=date
        obj.time = time
        obj.description=decription
        obj.DAYCARE_id = request.session['did']
        obj.save()

        return HttpResponse("<script>alert('successs');window.location='/add_meeting#aa'</script>")


def add_teacher(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'admin/add teacher.html')

#
# class FilesystemStorage(object):
#     pass


def add_teacher_post(request):
    First_name = request.POST['first_name']
    Last_name = request.POST['last_name']
    Designation = request.POST['designation']
    Email = request.POST['email']
    Phone = request.POST['phone']
    Place = request.POST['place']

   
    # Create login entry for the teacher
    pwd = random.randint(1000, 9999)
    login_obj = login.objects.create(username=Email, password=pwd, usertype='teacher')

    # Save teacher details
    teacher_obj = teacher.objects.create(
        First_name=First_name,
        Last_name=Last_name,
        Designation=Designation,
        Email=Email,
        Phone=Phone,
        Place=Place,
        LOGIN=login_obj  # Linking login entry
    )

    # Sending email with login credentials
    try:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("your-email@gmail.com", "your-email-password")
        
        msg = MIMEMultipart()
        msg['From'] = "your-email@gmail.com"
        msg['To'] = Email
        msg['Subject'] = "Your Password for Daycare Website"
        body = f"Hello {First_name},\n\nYour login credentials:\nUsername: {Email}\nPassword: {pwd}\n\nPlease change your password after login."
        msg.attach(MIMEText(body, 'plain'))
        
        s.send_message(msg)
        s.quit()
    except Exception as e:
        print(f"Email sending failed: {e}")

    return HttpResponse("<script>alert('Teacher added successfully');window.location='/add_teacher#aa'</script>")


def assign_teacher(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/assign_teacher.html')

def assign_teacher_post(request):
    teacher_name=request.POST['textfield']
    Day=request.POST['textfield2']
    Hour=request.POST['textfield3']
    return HttpResponse("<script>alert('successs');window.location='/assign_teacher#aa'</script>")

def edit_facility(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = daycare_facility.objects.get(id=id)
    return render(request, 'Daycare/edit_facility.html',{"data":data})

def edit_facility_post(request,id):
    Facility=request.POST['textfield']
    description=request.POST['textarea']
    daycare_facility.objects.filter(id=id).update(facility=Facility, description=description)
    return HttpResponse("<script>alert('successs');window.location='/view_facility#aa'</script>")

def delete_facility(request,id):

    daycare_facility.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted successfully');window.location='/view_facility#aa'</script>")

def edit_fee(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = fee.objects.get(id=id)
    return render(request, 'Daycare/edit_fee.html', {"data": data})

def edit_fee_post(request,id):
    fees2=request.POST['textfield']
    age_group=request.POST['select']
    data = fee.objects.filter(age_group=age_group, DAYCARE = request.session['did'])

    if data.exists():
        return HttpResponse("<script>alert('fee already added');window.location='/view_fee#aa'</script>")
    else:
        fee.objects.filter(id=id).update(fee1=fees2, age_group=age_group)

        return HttpResponse("<script>alert('successs');window.location='/view_fee#aa'</script>")

def delete_fee(request,id):
    fee.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted successfully');window.location='/view_fee#aa'</script>")




def edit_meeting(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = meeting.objects.get(id=id)
    return render(request, 'Daycare/edit_meeting.html', {"data": data,"id":id})

def edit_meeting_post(request,id):
    date = request.POST['textfield']
    time = request.POST['textfield2']
    description= request.POST['textarea']
    meeting.objects.filter(id=id).update(date=date,time=time ,description=description)
    return HttpResponse("<script>alert('successs');window.location='/view_meeting#aa'</script>")

def delete_meeting(request,id):
    meeting.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted successfully');window.location='/view_meeting#aa'</script>")


def edit_teacher(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = teacher.objects.get(id=id)
    return render(request, 'admin/edit_teacher.html', {"data": data})

def edit_teacher_post(request,id):
    # try:
    #     teacher_name = request.POST['name']
    #     experience = request.POST['experience']
    #     email = request.POST['email']
    #     phone_number = request.POST['phone_number']
    #     Place = request.POST['place']
    #     qualifications = request.POST['qualification']
    #     imagee = request.FILES['photo']
    #     id_proof = request.FILES['aa']
    #     d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #     f = FileSystemStorage()
    #     f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\idproof\\" + d + '.pdf', id_proof)
    #     f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\photo\\" + d + '.jpg', imagee)
    #     f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\qualification\\" + d + '.pdf', qualifications)
    #     path1 = "/static/idproof/" + d + ".pdf"
    #     path2 = "/static/photo/" + d + ".jpg"
    #     path3 = "/static/qualification/" + d + ".pdf"
    #
    #     teacher.objects.filter(id=id).update(teacher_name=teacher_name, experience=experience, email=email,
    #                                          phone_number=phone_number, place=Place, id_proof=path1, imagee=path2,
    #                                          qualification=path3)
    #     return HttpResponse("<script>alert('Edited successfully');window.location='/view_teacher'</script>")
    #
    # except Exception as e:
    #     teacher_name = request.POST['name']
    #     experience = request.POST['experience']
    #     email = request.POST['email']
    #     phone_number = request.POST['phone_number']
    #     Place = request.POST['place']
    #
    #
    #     teacher.objects.filter(id=id).update(teacher_name=teacher_name, experience=experience, email=email,
    #                                          phone_number=phone_number, place=Place)
    #     return HttpResponse("<script>alert('Edited successfully');window.location='/view_teacher'</script>")




        teacher_name = request.POST['name']
        experience = request.POST['experience']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        place = request.POST['place']

        teacher.objects.filter(id=id).update(teacher_name=teacher_name, experience=experience,
                                             email=email,
                                             phone_number=phone_number, place=place)


        if 'aa' in request.FILES:

            idd = request.FILES['aa']
            d =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            f = FileSystemStorage()
            f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\idproof\\" + d + '.pdf', idd)
            path = "/static/idproof/" + d + ".pdf"
            teacher.objects.filter(id=id).update(id_proof=path)


        if 'qualification' in  request.FILES:

            qualification = request.FILES['qualification']
            d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            f = FileSystemStorage()
            f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\qualification\\" + d + '.pdf', qualification)
            path2 = "/static/qualification/" + d + ".pdf"
            teacher.objects.filter(id=id).update(qualification= path2)


        if 'photo' in request.FILES:

            imagee = request.FILES['photo']
            d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            f = FileSystemStorage()
            f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\photo\\" + d + '.jpg', imagee)
            path1 = "/static/photo/" + d + ".jpg"
            teacher.objects.filter(id=id).update(photo=path1 )




        return HttpResponse("<script>alert('Edited successfully');window.location='/view_teacher#aa'</script>")

def delete_teacher(request,id):
    login.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted successfully');window.location='/view_teacher#aa'</script>")


def Register(request):
    # if 'lid' not in request.session:
    #     return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/register_index.html')

def Register_post(request):
    Name = request.POST['textfield']
    import datetime
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dt1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs = FileSystemStorage()

    # Save photo and license files

    # Define the file paths to be stored in the database
    path = '/static/photo/' + dt + '.jpg'

    # Collect relevant form data
    Place = request.POST['textfield2']
    Post = request.POST['textfield3']
    Pin = request.POST['textfield4']
    Latitude = request.POST['lat']
    Longitude = request.POST['long']
    Email = request.POST['textfield7']
    Phone = request.POST['textfield8']
    Enter_password = request.POST['textfield9']
    confirm_password = request.POST['textfield10']

    # Check if the email already exists
    data = login.objects.filter(username=Email)
    if data.exists():
        return HttpResponse("<script>alert('email already exists');window.location='/'</script>")
    else:
        # Ensure passwords match before creating the user
        if Enter_password == confirm_password:
            # Create login entry
            obj1 = login()
            obj1.username = Email
            obj1.password = Enter_password
            obj1.usertype = "parent"
            obj1.save()

            # Create parent entry, including only fields in the parent model
            obj = parent()
            obj.name = Name
            obj.email = Email
            obj.phone_number = Phone  # Storing phone number
            obj.place = Place
            obj.post = Post
            obj.pincode = Pin
            obj.latitude = Latitude
            obj.longitude = Longitude
            obj.LOGIN = obj1
            obj.save()

            return HttpResponse("<script>alert('successs');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('password mismatch');window.location='/'</script>")




def manage_profile(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = parent.objects.get(LOGIN=request.session['lid'])
    return render(request, 'Daycare/update.html',{"data":data})

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime

def manage_profile_post(request):
    try:
        # Fetching form data from the form fields
        name = request.POST['textfield']
        place = request.POST['textfield2']
        post = request.POST['textfield3']
        pin = request.POST['textfield4']
        gender = request.POST['textfield5']
        age = request.POST['textfield6']
        latitude = request.POST['textfield7']  # Corrected for latitude field
        longitude = request.POST['textfield8']  # Corrected for longitude field
        phone_number = request.POST['textfield10']  # Corrected phone number field

        # Handling photo upload
        if 'fileField1' in request.FILES:
            photo = request.FILES['fileField1']
            fs = FileSystemStorage()
            dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            photo_path = fs.save(f"photos/{dt}.jpg", photo)
            photo_url = fs.url(photo_path)
        else:
            photo_url = None  # In case no photo is uploaded
        
        # Update the parent model instance
        parent_instance = parent.objects.filter(LOGIN=request.session['lid']).first()
        if parent_instance:
            parent_instance.name = name
            parent_instance.place = place
            parent_instance.post = post
            parent_instance.pincode = pin
            parent_instance.gender = gender
            parent_instance.age = age
            parent_instance.latitude = latitude
            parent_instance.longitude = longitude
            parent_instance.phone_number = phone_number
            if photo_url:
                parent_instance.photo = photo_url  # Update photo only if uploaded
            parent_instance.save()

            return HttpResponse("<script>alert('Success');window.location='/manage_profile'</script>")
        else:
            return HttpResponse("<script>alert('Parent not found');window.location='/manage_profile'</script>")

    except Exception as e:
        print(e)  # Log the exception for debugging
        return HttpResponse("<script>alert('An error occurred. Please try again.');window.location='/'</script>")


def view_all_students(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = student.objects.all()
    return render(request, 'Daycare/view_all_students.html',{'rrrr':data})

def view_assign(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/view_assign.html')

def view_attendance(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = attendance.objects.filter(STUDENT=id)
    return render(request, 'Daycare/view_attendance.html',{'mmmm':data})

def view_facility(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data=daycare_facility.objects.filter(DAYCARE__LOGIN=request.session['lid'])

    return render(request, 'Daycare/view_facility.html',{'vie':data})


def view_food_menu_new(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")
    return  HttpResponse("<script>window.location='/add_photo_video'</script>")
    # data = food_menu.objects.filter(DAYCARE__LOGIN=request.session['lid'])
    # data = food_menu.objects.filter(DAYCARE__LOGIN = request.session['lid'])

    # return render(request,'Daycare/view_food_menu.html',{'data':data})

def edit_food_menu(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data=food_menu.objects.get(id=id)
    return render(request, 'Daycare/edit_food_menu.html',{"data":data})

def edit_food_menu_post(request,id):
   try:
       day = request.POST['select2']
       food = request.POST['textfield2']
       info = request.POST['select']



       food_menu.objects.filter(id=id).update(day=day, food=food, info=info)
       return HttpResponse("<script>alert('Edited successfully');window.location='/view_food_menu_new#aa'</script>")
   except Exception as e:
       day = request.POST['select2']
       food = request.POST['textfield2']
       info = request.POST['textfield3']
       food_menu.objects.filter(id=id).update(day=day, food=food, info=info)
       return HttpResponse("<script>alert('Edited successfully');window.location='/view_food_menu_new#aa'</script>")

def delete_food_menu(request,id):
    food_menu.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted successfully');window.location='/view_food_menu_new#aa'</script>")


def view_meeting(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = meeting.objects.filter(DAYCARE__LOGIN=request.session['lid'])
    return render(request, 'Daycare/view_meeting.html', {'jee': data})


def view_payment(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = payment.objects.filter(DAYCARE_REQUEST__DAYCARE=request.session['did'])
    ar=[]
    st=student.objects.all()
    return render(request, 'Daycare/view_payment.html',{'kee': data})

def view_performance(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = performance.objects.filter(STUDENT=id)
    return render(request, 'Daycare/view_performance.html',{'loo':data})

def view_daycare_rating(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = rating.objects.filter(DAYCARE__LOGIN=request.session['lid'])
    return render(request,"Daycare/view_rating.html",{"data":data})
    # return render(request, 'Daycare/view_rating.html',{'data': data})

def view_request_from_parent(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = daycare_request.objects.filter(DAYCARE__LOGIN=request.session['lid'],status="pending")
    return render(request, 'Daycare/view_request_from_parent.html',{'wee': data})

def approve_request(request,id):
    daycare_request.objects.filter(id=id).update(status="approved")
    return HttpResponse("<script>alert('successs');window.location='/approved_request'</script>")

def reject_request(request,id):
    daycare_request.objects.filter(id=id).update(status="rejected")
    return HttpResponse("<script>alert('successs');window.location='/view_request_from_parent'</script>")

def approved_request(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = daycare_request.objects.filter(DAYCARE__LOGIN=request.session['lid'], status="approved")
    return render(request, 'Daycare/view_verified_request.html', {'data': data})


def view_teachers(request, id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = teacher.objects.filter(DAYCARE__LOGIN=request.session['lid'])
    # assigned_teachers = assign.objects.values_list('TEACHER_id', flat=True)

    # for i in data:
    #     i.is_assigned = i.id in assigned_teachers



    return render(request, 'Daycare/assign_teachers.html', {'aaa': data, "id": id})


def assignn(request,id,tid):
    data = assign.objects.filter(TEACHER_id=id,DAYCARE_REQUEST_id=tid)
    if data.exists():
        return HttpResponse("<script>alert('Already Assigned');window.location='/approved_request#aa'</script>")
    else:
        obj=assign()
        obj.date=datetime.datetime.now()
        obj.TEACHER_id=id
        obj.DAYCARE_REQUEST_id=tid
        obj.save()
        return HttpResponse("<script>alert('Assigned');window.location='/approved_request#aa'</script>")




def view_teacher(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = teacher.objects.all()
    return render(request, 'admin/view_teacher.html', {'aaa': data})

def view_verified_request(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Daycare/view_verified_request.html')

def daycare_change_password(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request,"Daycare/change password.html")


def daycare_change_password_post(request):
    Current_password=request.POST['textfield']
    New_password=request.POST['textfield2']
    Confirm_password=request.POST['textfield2']
    data = login.objects.filter(id=request.session['lid'],password=Current_password)
    if data.exists():
        if New_password == Confirm_password:
            login.objects.filter(id=request.session['lid']).update(password=Confirm_password)
            return HttpResponse("<script>alert('Success');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('Failed');window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('Not Found');window.location='/'</script>")

def daycare_home(request):
    return render(request, 'Daycare/daycare_index.html')







#------------------------ Teacher =----------


def view_charges(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data=assign.objects.filter(TEACHER__LOGIN=request.session['lid'])
    return render(request, 'Teacher/view_charges.html',{'wer':data})


def view_all_student(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    # data = student.objects.all()
    #
    # for i in data:
    data= daycare_request.objects.filter(status="approved")


    return render(request, 'Teacher/view_all_student.html', {'lll': data})


def add_attendance1(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Teacher/add_attendance.html',{'id':id})


def add_attendance_post(request,id):
    attendance1=request.POST['select']
    date = datetime.datetime.now().strftime("%y-%m-%d")

    data = attendance.objects.filter(date=date, STUDENT_id=id)

    if data.exists():
        return HttpResponse("<script>alert('attendance already added');window.location='/add_attendance1/"+str(id)+"#aa'</script>")
    else:

        obj=attendance()
        obj.attendance1=attendance1
        obj.date=date
        obj.STUDENT_id = id
        obj.TEACHER_id = teacher.objects.get(LOGIN_id=request.session['lid']).id
        obj.save()

        return HttpResponse("<script>alert('successs');window.location='/add_attendance1/"+str(id)+"#aa'</script>")


def edit_attendance(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = attendance.objects.get(id=id)
    return render(request, 'Teacher/edit_attendance.html',{"data":data})


def edit_attendance_post(request,id):
    attendance1=request.POST['select']
    date=datetime.datetime.now().strftime("%y-%m-%d")


    attendance.objects.filter(id=id).update(attendance1=attendance1, date=date)
    s=request.session['studid']
    return HttpResponse("<script>alert('successs');window.location='/view_attendance1/"+str(s)+"#aa'</script>")

def delete_attendance(request,id):
    attendance.objects.get(id=id).delete()
    sid = request.session['studid']
    return HttpResponse("<script>alert('Deleted successfully');window.location='/view_attendance1/" + sid + "#aa'</script>")


def view_attendance1(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = attendance.objects.filter(STUDENT_id=id)
    request.session['studid'] = id
    return render(request, 'Teacher/view_attendance.html', {'ppp': data})




def add_performance(request, id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Teacher/add_performance.html', {'id':id})


def add_performance_post(request,id):

    performance1=request.POST['textfield']
    date=request.POST['textfield4']
    mark=request.POST['textfield2']
    category=request.POST['textfield3']

    data = performance.objects.filter(performance1=performance1,date=date,category=category,mark=mark, STUDENT_id=request.session['lid'])

    if data.exists():
        return HttpResponse("<script>alert('performance already added');window.location='/add_performance#aa'</script>")

    obj=performance()
    obj.performance1=performance1
    obj.date=date
    obj.mark=mark
    obj.category=category
    obj.STUDENT_id = id
    obj.TEACHER_id = teacher.objects.get(LOGIN_id=request.session['lid']).id
    obj.save()

    return HttpResponse("<script>alert('successs');window.location='/view_performance1/"+id+"#aa'</script>")

def view_performance1(request, id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = performance.objects.filter(STUDENT_id=id)
    request.session['stuid']=id
    return render(request, 'Teacher/view_performance.html',{'vvv':data})

def edit_performance(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data = performance.objects.get(id=id)
    return render(request, 'Teacher/edit_performance.html', {"data": data})

def edit_performance_post(request,id):
    performance1=request.POST['textfield']
    date=request.POST['textfield2']
    mark=request.POST['textfield3']
    category=request.POST['textfield4']
    # s=request.session['studid']
    performance.objects.filter(id=id).update(performance1=performance1,  category=category, date=date , mark=mark)

    return HttpResponse("<script>alert('Edited successfully');window.location='/view_performance1/"+id+"#aa'</script>")

def delete_performance(request,id):
    performance.objects.get(id=id).delete()
    s=request.session['studid']
    return HttpResponse("<script>alert('deleted successfully');window.location='/view_performance1/"+str(s)+"#aa'</script>")

def change_password1(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Teacher/change_pass.html')

def change_password1_post(request):
    Current_password = request.POST['textfield']
    New_password = request.POST['textfield2']
    Confirm_password = request.POST['textfield3']
    data = login.objects.filter(id=request.session['lid'], password=Current_password)
    if data.exists():
        if New_password == Confirm_password:
            login.objects.filter(id=request.session['lid']).update(password=Confirm_password)
            return HttpResponse("<script>alert('Success');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('Failed');window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('Not Found');window.location='/'</script>")


def send_notification(request,id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Teacher/send_notification.html',{'id':id})

def send_notification_post(request,id):
    date=datetime.datetime.now().strftime("%y-%m-%d")
    content=request.POST['textfield2']

    obj=notification()
    obj.date=date
    obj.content=content
    obj.ASSIGN_id = id
    obj.save()
    return HttpResponse("<script>alert('successs');window.location='/view_charges#aa'</script>")



def view_meeting1(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    tchr=teacher.objects.get(LOGIN=request.session['lid'])
    data = meeting.objects.filter(DAYCARE=tchr.DAYCARE)
    return render(request, 'Teacher/view_meeting.html',{'qwe':data})


def view_rating1(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    tchr = teacher.objects.get(LOGIN=request.session['lid'])
    data = rating.objects.filter(DAYCARE=tchr.DAYCARE)
    return render(request, 'Teacher/view_rating.html',{'uio':data})


def teacher_home(request):
    return render(request, 'Teacher/teacher_index.html')


# user android

def and_login(request):
    username=request.POST['username']
    password=request.POST['password']
    print("username",username)
    print("password",password)
    data=login.objects.filter(username=username,password=password)
    if data.exists():
        lid=data[0].id
        return JsonResponse({"status":"ok","lid":lid,"type":"parent"})
    else:
        return JsonResponse({"status":None})





def register(request):

    nm = request.POST['name']

    ph = request.POST['phone_number']
    em = request.POST['email']
    pl = request.POST['place']
    pos = request.POST['post']
    pi = request.POST['pin']
    gen = request.POST['gender']
    age = request.POST['age']
    lat =  request.POST['latitude']
    lon = request.POST['longitude']
    pas = request.POST['password']
    con = request.POST['confirm_password']
    print("lattttt", lat)
    if pas == con:
        obj1=login()
        obj1.username  = em
        obj1.password = pas
        obj1.usertype='parent'
        obj1.save()

        obj = parent()
        obj.name = nm
        obj.phone_number = ph
        obj.email = em
        obj.place = pl
        obj.post = pos
        obj.pincode = pi
        obj.gender = gen
        obj.age = age
        obj.latitude = lat
        obj.longitude = lon
        obj.LOGIN = obj1
        obj.save()
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": None})


def add_children(request):

    nm= request.POST['nm']
    ag= request.POST['age']
    gen=request.POST['gender']
    bio=request.POST['bio']
    pho=request.FILES['pic']
    lid = request.POST['lid']
    drid = request.POST['drid']
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    f = FileSystemStorage()
    f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\photo\\" + d + '.jpg', pho)
    path2 = "/static/photo/" + d + ".jpg"
    data = student.objects.filter(student_name=nm,PARENT__LOGIN=lid)
    if data.exists():
        return JsonResponse({"status": None})

    obj=student()
    obj.student_name=nm
    obj.age=ag
    obj.gender=gen
    obj.bio=bio
    obj.photo=path2
    obj.PARENT_id = parent.objects.get(LOGIN=lid).id
    obj.DAYCARE_id = drid
    obj.save()

    return JsonResponse({"status": "ok"})

def view_children(request):

    did = request.POST['drid']
    print(("didddddddddddd",did))
    lid = request.POST['lid']
    res=student.objects.filter(PARENT__LOGIN=lid,DAYCARE_id=did)
    ar=[]
    for i in res:
        ar.append(
            {
                "name":i.student_name,
                "cid":i.id,
                "age":i.age,
                "gender":i.gender,
                "photo":i.photo,
                "bio":i.bio
            }
        )
        print("chillllllllllll",ar)
    return JsonResponse({"status": "ok","data":ar})

def edit_children(request):

    cid = request.POST['cid']
    data = student.objects.get(id=cid)
    return JsonResponse({"status": "ok","name":data.student_name,"age":data.age,"bio":data.bio,"image":data.photo})


def edit_children_post(request):
    try:
        cid = request.POST['cid']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        bio = request.POST['bio']
        # s = request.session['studid']
        pho = request.FILES['pic']
        d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        f = FileSystemStorage()
        f.save(r"C:\Users\Admin\PycharmProjects\Daycare\DaycareApp\static\photo\\" + d + '.jpg', pho)
        path2 = "/static/photo/" + d + ".jpg"

        student.objects.filter(id=cid).update(student_name=name, age=age, gender=gender, bio=bio, photo=path2)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        cid = request.POST['cid']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        bio = request.POST['bio']
        # s = request.session['studid']

        student.objects.filter(id=cid).update(student_name=name, age=age, gender=gender, bio=bio)

        return JsonResponse({"status": "ok"})


def delete_children(request):
    cid=request.POST['cid']
    student.objects.get(id=cid).delete()
    return JsonResponse({"status": "ok"})

def view_nearby_daycare_rating(request):

    res = daycare.objects.filter(LOGIN__usertype='daycare')
    ar = []
    for i in res:
        print(i.license,"uuuuuuuu")
        ar.append(
            {

                "drid":i.id,
                "dname":i.name,
                "email":i.email,
                "contact":i.phone,
                "place":i.place,
                "post":i.post,
                "pin":i.pin,
                "license":i.license,
                "photo":i.photo,
                "latitude":i.latitude,
                "longitude":i.longitude
            }
        )
    return JsonResponse({"status": "ok","data":ar})

def view_teacherss(request):

    dr =request.POST['drid']
    res = teacher.objects.filter(DAYCARE_id=dr)
    ar = []
    for i in res:
        ar.append(
            {
                "tid": i.id,
                "qualification": i.qualification,
                "phone_number": i.phone_number,
                "experience": i.experience,
                "id_proof":i.id_proof,
                "teacher_name":i.teacher_name,
                "email": i.email,
                "photo": i.photo,
                "place": i.place
            }
        )
    return JsonResponse({"status": "ok","data":ar})

def view_facilities(request):
    drid  = request.POST['drid']
    res = daycare_facility.objects.filter(DAYCARE=drid)
    ar = []
    for i in res:
        ar.append(
            {
                "fid": i.id,
                "facility": i.facility,
                "description": i.description

            }
        )
    return JsonResponse({"status": "ok","data":ar})

def view_fees(request):
    dr = request.POST['drid']
    res = fee.objects.filter(DAYCARE_id=dr)

    ar = []
    for i in res:
        ar.append(
            {
                "ffid": i.id,
                "fee1": i.fee1,
                "age_group": i.age_group

            }
        )
    return JsonResponse({"status": "ok","data":ar})

def view_food_menu(request):
    drid = request.POST['drid']
    res = food_menu.objects.filter(DAYCARE=drid)
    ar = []
    for i in res:
        ar.append(
            {
                "foid": i.id,
                "day": i.day,
                "info": i.info,
                "food": i.food



            }
        )
    return JsonResponse({"status": "ok","data":ar})

def send_request_to_daycare(request):

    dr = request.POST['drid']
    ci = request.POST['cid']

    data = daycare_request.objects.filter(DAYCARE=dr,STUDENT=ci)
    if data.exists():
        return JsonResponse({"status": "notok"})
    else:
        obj=daycare_request()
        obj.date=datetime.datetime.now().date()
        obj.status='pending'
        obj.assigned_status='pending'
        obj.DAYCARE_id = dr
        obj.STUDENT_id=ci
        # obj.STUDENT_id = 1
        obj.save()
        return JsonResponse({"status": "ok"})

def view_request_status(request):

    lid = request.POST['lid']

    res = daycare_request.objects.filter(STUDENT__PARENT__LOGIN=lid)
    ar = []
    for i in res:
        res = daycare_request.objects.filter(id=i.id)
        daycare_id = res[0].DAYCARE.id
        fe = fee.objects.filter(DAYCARE_id=daycare_id)
        fe1=fe[0].fee1
        print(fe,"feeeeee")
        ar.append(
            {
                "rsid": i.id,
                "date": i.date,
                "dname": i.DAYCARE.name,
                "contact":i.DAYCARE.phone,
                "status":i.status,
                "amount":fe1,
                "student":i.STUDENT.student_name,

            }
        )

        print(ar,"aaaaaaaaaaaaaaaa")

    return JsonResponse({"status": "ok","data":ar})

def view_class__incharge(request):

    lid = request.POST['lid']

    res = assign.objects.filter(DAYCARE_REQUEST__STUDENT__PARENT__LOGIN=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "iid": i.id,
                "date": i.date,
                "tname": i.TEACHER.teacher_name,
                "contact":i.TEACHER.phone_number,
                "dname":i.TEACHER.DAYCARE.name,
                "student":i.DAYCARE_REQUEST.STUDENT.student_name,

            }
        )
    return JsonResponse({"status": "ok", "data": ar})

def make_call(request):
    return JsonResponse({"status": "ok"})

def view_notifications(request):

    lid = request.POST['lid']

    res = notification.objects.filter(ASSIGN__DAYCARE_REQUEST__STUDENT__PARENT__LOGIN=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "nid": i.id,
                "date": i.date,
                "content": i.content,
                "student":i.ASSIGN.DAYCARE_REQUEST.STUDENT.student_name,


            }
        )
    return JsonResponse({"status": "ok", "data": ar})

def view_atendances(request):

    lid = request.POST['lid']

    res = attendance.objects.filter(STUDENT__PARENT__LOGIN=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "aid": i.id,
                "attendance": i.attendance1,
                "date": i.date,
                "student":i.STUDENT.student_name,

            }
        )
    return JsonResponse({"status": "ok", "data": ar})

def view_performances(request):

    lid = request.POST['lid']

    res = performance.objects.filter(STUDENT__PARENT__LOGIN=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "pid": i.id,
                "performance": i.performance1,
                "date": i.date,
                "category":i.category,
                "mark":i.mark,
                "student":i.STUDENT.student_name,

            }
        )
    return JsonResponse({"status": "ok", "data": ar})

def view_meetings(request):

    res = meeting.objects.all()
    ar = []
    for i in res:
        ar.append(
            {
                "mid": i.id,
                "date": i.date,
                "time": i.time,
                "description":i.description,
                "daycare":i.DAYCARE.name,

            }
        )
    return JsonResponse({"status": "ok", "data": ar})

def send_rating(request):

    dr = request.POST['did']
    pid = request.POST['lid']
    rt = request.POST['rating']
    print("daycare_id",dr)
    print("parent_id",pid)
    print("rating",rt)

    data = rating.objects.filter(PARENT__LOGIN=pid,DAYCARE_id = dr)
    print("dataaaaa",data)
    if data.exists():
        rating.objects.filter(PARENT__LOGIN=pid).update(rating=rt,date =datetime.datetime.now().date())
    else:

        obj = rating()


        obj.date =datetime.datetime.now().date()

        obj.DAYCARE_id = dr
        obj.PARENT = parent.objects.get(LOGIN=pid)
        obj.rating = rt
        obj.save()
    return JsonResponse({"status": "ok"})


def send_complaint(request):

    dr = request.POST['drid']
    pid = request.POST['lid']
    cmp =request.POST['complaint']
    obj=complaint()

    obj.complaint_date = datetime.datetime.now().date()
    obj.reply = "pending"
    obj.reply_date ="pending"
    obj.DAYCARE_id=dr
    obj.PARENT = parent.objects.get(LOGIN=pid)
    obj.complaint=cmp
    obj.save()
    return JsonResponse({"status": "ok"})

def view_reply(request):

    lid = request.POST['lid']
    drid = request.POST['drid']

    res = complaint.objects.filter(PARENT__LOGIN=lid,DAYCARE=drid)


    ar = []
    for i in res:
        ar.append(
            {
                "rid": i.id,
                "complaint": i.complaint,
                "date": i.complaint_date,
                "reply":i.reply,
                "reply_date":i.reply_date


            }

        )

    return JsonResponse({"status": "ok", "data": ar})

def view_feedbacks(request):
    drid = request.POST['drid']

    res = feedback.objects.filter(DAYCARE=drid)
    ar = []
    for i in res:
        ar.append(
            {
                "feid": i.id,
                "feedback": i.feedback,
                "date": i.date

            }
        )
    return JsonResponse({"status": "ok","data":ar})

# def change_pass(request):
#     return JsonResponse({"status": "ok"})


def change_pass(request):
    lid = request.POST['lid']
    Current_password=request.POST['current_password']
    New_password=request.POST['new_password']
    Confirm_password=request.POST['confirm_Password']
    data = login.objects.filter(id=lid,password=Current_password)
    if data.exists():
        if New_password == Confirm_password:
            login.objects.filter(id=lid).update(password=Confirm_password)
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"status": "no"})

    else:
        return JsonResponse({"status": None})



def send_feedback(request):

        dr = request.POST['drid']
        pid = request.POST['lid']
        cmp = request.POST['feedback']
        obj = feedback()

        obj.date = datetime.datetime.now().date()

        obj.DAYCARE_id = dr
        obj.PARENT = parent.objects.get(LOGIN=pid)
        obj.feedback = cmp
        obj.save()


        return JsonResponse({"status": "ok"})



# ==================== PAYMENT ================

def android_online_payment(request):
    rs = request.POST['rsid']
    am= request.POST['amount']

    print("rsssssssssss",rs)
    print("ammmmmmmmm",am)


    obj = payment()
    obj.amount = am
    obj.date = datetime.datetime.now().date()
    obj.payment_status = "online"

    obj.DAYCARE_REQUEST_id = rs
    obj.save()

    return JsonResponse({"status": "ok"})

def android_offline_payment(request):
    md = request.POST['mode']
    rs = request.POST['rsid']
    res = daycare_request.objects.filter(id=rs)
    daycare_id = res[0].DAYCARE.id
    fe= fee.objects.filter(DAYCARE=daycare_id)
    fe1=fe[0].fee1


    print(md)
    print(rs)
    obj = payment()
    obj.amount = fe1
    obj.date = datetime.datetime.now().date()
    obj.payment_status = "offline"


    obj.DAYCARE_REQUEST_id = rs

    obj.save()

    return JsonResponse({"status": "ok"})


def view_ratings(request):

    dr = request.POST['did']
    res = rating.objects.filter(DAYCARE_id=dr)
    ar = []
    for i in res:
        ar.append(
            {
                "vrid": i.id,
                "date": i.date,
                "rating": i.rating,

            }
        )
        print(ar)
    return JsonResponse({"status": "ok","data":ar})

def view_profile(request):

    dr = request.POST['lid']
    res = parent.objects.get(LOGIN=dr)

    return JsonResponse({"status": "ok","name":res.name,"age":res.age,"ph":res.phone_number,"email":res.email,"place":res.place,"post":res.post,"pin":res.pincode,"gender":res.gender})


def edit_profiles(request):

    lid = request.POST['lid']
    name = request.POST['n']
    age = request.POST['age']
    phone = request.POST['p']
    email = request.POST['e']
    place = request.POST['pl']
    post = request.POST['postt']
    pin = request.POST['piii']
    gend = request.POST['gender']
    print("genderrrrrrr",gend)


    parent.objects.filter(LOGIN=lid).update(name=name, age=age,gender=gend, phone_number=phone, email=email, place=place, post=post, pincode=pin)



    return JsonResponse({"status": "ok"})




def forgot_password(request):
    email=request.POST['username']
    data = login.objects.filter(username=email)
    if data.exists():
        pwd = data[0].password

        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("jasijaseer06@gmail.com", "wkxf jffn jsda qogm")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "jasijaseer06@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Daycare App"
        body = "Your password"+str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

    return JsonResponse({"status": "ok"})


def forgot_pass(request):

    return render(request, 'index.html')

def forgot_pass_post(request):
    email = request.POST['username']
    data = login.objects.filter(username=email)
    if data.exists():
        pwd = data[0].password

        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("jasijaseer06@gmail.com", "wkxf jffn jsda qogm")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "jasijaseer06@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Daycare"
        body = "Your password" + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return HttpResponse("<script>alert('password sended to email');window.location='/'</script>")

#preschool


def view_parent(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    data=parent.objects.all()
    return render(request,"admin/view parent.html",{'data':data})


from django.shortcuts import render
from django.http import HttpResponse

def add_activities(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    return render(request, 'Teacher/add_activities.html', {'id': request.session['lid']})

def add_activities_post(request, id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    # Get the posted data
    activity_name = request.POST['activity_name']
    date = request.POST['textfield4']
    description = request.POST['description']

    # Check if the activity already exists for this teacher
    data = Activity.objects.filter(activity_name=activity_name, date=date, description=description)
    if data.exists():
        return HttpResponse("<script>alert('Activity already added');window.location='/add_activities'</script>")

    # Create and save the activity
    obj = Activity()
    obj.activity_name = activity_name
    obj.date = date
    obj.description = description

    # Associate the activity with the teacher (using the id passed to the form)
    teacher_instance = teacher.objects.get(LOGIN_id=request.session['lid'])  # Fixed the variable name here
    obj.teacher = teacher_instance  # Now using teacher_instance instead of teacher
    obj.save()

    return HttpResponse("<script>alert('Activity added successfully');window.location='/add_activities'</script>")  

def add_student(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")
    
    # Pass parent_id as context to the template
    return render(request, 'Daycare/add_student.html', {'parent_id': request.session['pid']})



def add_student_post(request, id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    if request.method == "POST":
        # Get the posted data
        student_name = request.POST['student_name']
        age = request.POST['age']
        gender = request.POST['gender']
        photo = request.FILES.get('photo')  # Make sure to use request.FILES for the photo
        bio = request.POST['bio']
        parent_id = id  # Assuming 'id' refers to the parent instance

        # Check if a student with the same name already exists for this parent (optional)
        existing_student = student.objects.filter(student_name=student_name, PARENT_id=parent_id)
        if existing_student.exists():
            return HttpResponse("<script>alert('Student already exists for this parent');window.location='/add_student'</script>")

        # Create and save the new student record
        obj = student()
        obj.student_name = student_name
        obj.age = age
        obj.gender = gender
        obj.photo = photo  # This will save the uploaded photo
        obj.bio = bio
        obj.PARENT_id = parent_id  # Associating the student with the parent using the parent ID
        obj.save()

        return HttpResponse("<script>alert('Student added successfully');window.location='/add_student'</script>")

def view_student_profile(request):
    # Check if the user is logged in (parent session check)
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    # Get the parent associated with the logged-in user (assuming 'lid' is the parent session ID)
    parent_id = request.session['pid']

    # Fetch the student(s) associated with the parent_id
    # If a parent has multiple students, you can display all students or pick one as needed
    students = student.objects.filter(PARENT_id=parent_id)

    
    # Render the template with the students' data
    return render(request, 'Daycare/view_student_profile.html', {'students': students})
        

def view_activities(request):
    # Check if the user is logged in (teacher session check)
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    # Fetch all activities (without filtering by teacher)
    activities = Activity.objects.all()

    # If no activities are found, show a message
    if not activities:
        return HttpResponse("<script>alert('No activities found');window.location='/add_activity'</script>")

    # Render the template with the activities
    return render(request, 'Daycare/view_activities.html', {'activities': activities})









from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import assign, teacher, student  # Import the relevant models

def assign_teacher(request, id):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")
    stud=student.objects.get(id=id)
    if request.method == 'POST':
        # Extract form data from POST request
        teacher_name = request.POST.get('textfield')  # Get teacher name or teacher ID
        Day = request.POST.get('textfield2')  # Get day (date) from the form
        Hour = request.POST.get('textfield3')  # Get hour (time) from the form

        try:
            # Assuming teacher_name is the ID of the teacher selected, adjust this if it's the name
            teacher_instance = teacher.objects.get(id=teacher_name)
            
            # Create a new assignment record
            assignment = assign(
                STUDENT_id=stud.id,  # Associate the student with the assignment
                TEACHER=teacher_instance,
                date=Day,
                assigned_status='assigned'  # Using Hour as the status for now
            )
            assignment.save()

            return HttpResponse("<script>alert('Assignment Successful');window.location='/admin_home#aa'</script>")
        except teacher.DoesNotExist:
            return HttpResponse("<script>alert('Teacher does not exist');window.location='/admin_home'</script>")

    # Handle GET request - render the form for assigning a teacher
    teachers = teacher.objects.all()  # Get all teachers
    students = student.objects.all()  # Get all students (if needed)
    
    return render(request, 'admin/assign_teacher.html', {'teachers': teachers, 'students': students})



from django.shortcuts import render
from .models import assign
from django.http import HttpResponse

def view_assigned_teacher(request):
    # Check if 'pid' (parent ID) exists in session
    if 'pid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")

    # Retrieve the assignments for the logged-in parent
    # Assuming the parent is associated with students through the 'PARENT' field in the 'student' model
    # Adjust query if your model has a different relationship

    parent_id = request.session['pid']
    
    # Fetch all students associated with the parent (assuming each student has a PARENT field)
    # Then, get the assignments for those students where the status is "assigned"
    assignments = assign.objects.filter(
        STUDENT__PARENT_id=parent_id,
        assigned_status="assigned"
    ).select_related('TEACHER', 'STUDENT')  # Use select_related for efficient querying

    # Pass the assignments and teacher info to the template
    return render(request, 'Daycare/view_assigned_teacher.html', {'assignments': assignments})




from django.shortcuts import render, redirect
from .models import Lesson, teacher, student
from django.core.files.storage import FileSystemStorage
import datetime




from django.shortcuts import render
from .models import assign
from .models import student  # Assuming 'student' is the name of your student model
from django.shortcuts import render
from django.http import HttpResponse
from .models import assign

def view_assigned_students(request):
    # Check if the teacher is logged in
    if 'tid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/';</script>")
    
    teacher_id = request.session['tid']  # Retrieve the teacher's session ID
    
    # Get all the assignments where the current teacher is assigned and the status is 'assigned'
    assigned_students = assign.objects.filter(TEACHER_id=teacher_id, assigned_status='assigned')
    
    # Check if any data is returned from the query
    if not assigned_students:
        print("No assigned students found for this teacher.")
    
    # Pass the data to the template for rendering
    return render(request, 'teacher/view_assigned_students.html', {'assigned_students': assigned_students})




from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
from .models import login, parent  # Ensure your models are imported correctly

def staff_register(request):
    if request.method == 'POST':
        # Handle the form submission
        Name = request.POST['textfield']
        import datetime
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs = FileSystemStorage()

        # Collect form data
        Place = request.POST['textfield2']
        Post = request.POST['textfield3']
        Pin = request.POST['textfield4']
        Email = request.POST['textfield7']
        Phone = request.POST['textfield8']
        Enter_password = request.POST['textfield9']
        confirm_password = request.POST['textfield10']

        # Check if the email already exists
        data = login.objects.filter(username=Email)
        if data.exists():
            return HttpResponse("<script>alert('Email already exists');window.location='/admin_home'</script>")

        # Ensure passwords match before creating the user
        if Enter_password == confirm_password:
            # Create login entry
            obj1 = login()
            obj1.username = Email
            obj1.password = Enter_password
            obj1.usertype = "staff"
            obj1.save()

            # Create parent entry, including only fields in the parent model
            obj = staff()
            obj.name = Name
            obj.email = Email
            obj.phone_number = Phone  # Storing phone number
            obj.place = Place
            obj.post = Post
            obj.pincode = Pin
            obj.LOGIN = obj1
            obj.save()

            return HttpResponse("<script>alert('Registration successful');window.location='/admin_home'</script>")
        else:
            return HttpResponse("<script>alert('Password mismatch');window.location='/admin_home'</script>")
    
    else:
        # If GET request, just render the form
        return render(request, 'admin/Register.html')



def staff_home(request):
    return render(request, 'staff/staff_index.html')


from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import student  # Ensure your model is imported correctly

def view_edit_student_profile(request):
    # Ensure the parent is logged in (this example uses session)
    parent_id = request.session.get('pid')
    if not parent_id:
        return HttpResponse("Unauthorized: Parent not logged in.")

    try:
        # Assuming each parent has one student profile
        student_obj = student.objects.get(PARENT_id=parent_id)
    except student.DoesNotExist:
        return HttpResponse("No student profile found.")

    if request.method == "POST":
        # Update profile data from POST values
        student_obj.student_name = request.POST.get("student_name", student_obj.student_name)
        student_obj.age = request.POST.get("age", student_obj.age)
        student_obj.gender = request.POST.get("gender", student_obj.gender)
        student_obj.bio = request.POST.get("bio", student_obj.bio)
        
        # Handle photo upload if provided
        if request.FILES.get("photo"):
            fs = FileSystemStorage()
            photo_file = request.FILES["photo"]
            filename = fs.save(photo_file.name, photo_file)
            student_obj.photo = fs.url(filename)
        
        student_obj.save()
        return HttpResponseRedirect('/view_edit_student_profile')  # Redirect after update

    # For GET request, display the student's data
    return render(request, 'Daycare/view_edit_student_profile.html', {'student': student_obj})


from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import Work, teacher, student  # adjust imports as needed

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Work, teacher, student

def add_work(request, id):
    # Ensure teacher is logged in; assume teacher's ID is stored in session as 'tid'
    teacher_id = request.session.get('tid')
    if not teacher_id:
        return HttpResponse("Unauthorized: Please log in as teacher.")
    
    try:
        teacher_obj = teacher.objects.get(id=teacher_id)
    except teacher.DoesNotExist:
        return HttpResponse("Teacher not found.")
    
    # Get the student object using the URL parameter 'id'
    try:
        student_obj = student.objects.get(id=id)
    except student.DoesNotExist:
        return HttpResponse("Student not found.")
    
    if request.method == "POST":
        # Get the form data
        work_description = request.POST.get("work_description")
        date = request.POST.get("date")
        
        # Validate required fields
        if not work_description or not date:
            return HttpResponse("All fields are required.")
        
        # Create the Work entry
        new_work = Work.objects.create(
            teacher=teacher_obj,
            student=student_obj,
            work_description=work_description,
            date=date
        )
        # Redirect to a page showing uploaded work (adjust URL as needed)
        return HttpResponseRedirect("/view_assigned_students")
    
    else:
        # For GET requests, display the add work form.
        return render(request, 'teacher/add_work.html', {'student': student_obj})


def view_photo_video(request, id):
    try:
        student_obj = student.objects.get(id=id)
    except student.DoesNotExist:
        return HttpResponse("Student not found.")
    
    # Retrieve all file entries for this student
    files = File.objects.filter(student=student_obj)
    
    return render(request, 'teacher/view_photo_video.html', {
        'student': student_obj,
        'files': files
    })


from django.shortcuts import render
from .models import Work

def view_works(request):
    parent_id = request.session.get('pid')  # Fetch parent ID from session
    
    if not parent_id:
        return HttpResponse("Unauthorized: Please log in as a parent.")

    works = Work.objects.filter(student__PARENT=parent_id)  # Fetch all work entries for the parent's child
    

    return render(request, 'daycare/view_works.html', {'works': works})


def upload_work(request,id):
    if request.method == "POST":
        file_url = request.POST.get("file")  # Since it's a CharField, expect a URL/path as input
        date = request.POST.get("date")

        if not id or not file_url or not date:
            return HttpResponse("All fields are required.")

        try:
            work_obj = Work.objects.get(id=id)
        except Work.DoesNotExist:
            return HttpResponse("Selected work not found.")

        # Create a new upload work entry
        UploadWork.objects.create(
            work=work_obj,
            file=file_url,
            date=date
        )

        return redirect("/daycare_home")  # Redirect after successful upload

    else:
        works = Work.objects.all()  # Fetch all work entries for selection
        return render(request, 'daycare/upload_work.html', {'works': works})
    

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fee, student

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fee, student

def staff_add_fees(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        amount = request.POST.get("amount")

        if not student_id or not amount:
            return HttpResponse("All fields are required.")

        try:
            student_obj = student.objects.get(id=student_id)
        except student.DoesNotExist:
            return HttpResponse("Student not found.")

        # Check if the student already has a fee entry
        if Fee.objects.filter(student=student_obj).exists():
            return HttpResponse("Fees have already been added for this student.")

        # Create a new fee entry
        Fee.objects.create(student=student_obj, amount=amount)

        return redirect("/view_studentfees")  # Redirect after successful fee addition

    else:
        students = student.objects.all()  # Fetch all students for selection
        return render(request, 'staff/add_fees.html', {'students': students})

    

def view_studentfees(request):
    fees = Fee.objects.all()  # Fetch all fees from the database
    return render(request, 'staff/view_fees.html', {'fees': fees})



from django.shortcuts import render
from .models import Fee, Payment, student, parent

def parent_view_fee(request):
    try:
        parent_obj = parent.objects.get(id=request.session['pid'])  # Fetch the logged-in parent
    except parent.DoesNotExist:
        return HttpResponse("Parent not found.")

    # Get the students associated with the parent
    students = student.objects.filter(PARENT=parent_obj)

    # Fetch fee details for those students
    fees = Fee.objects.filter(student__in=students)

    # Fetch payment details for those students
    payments = Payment.objects.filter(student__in=students)

    return render(request, 'DAYCARE/view_fees.html', {'fees': fees, 'payments': payments})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from .models import Fee, Payment, student
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from .models import Fee, Payment



def pay_fees(request, id):
    fee = Fee.objects.get(id=id)

    if request.method == "POST":
        # Record the payment
        Payment.objects.create(
            student=fee.student,
            amount=fee.amount,
            month=now().strftime("%B"),  # Get current month
            date=now().strftime("%Y-%m-%d")  # Get current date
        )

        # Update fee status to "Paid"
        fee.status = "Paid"
        fee.save()

        return HttpResponse(f"<script>alert('Paid');window.location='/parent_view_fee'</script>")

    return render(request, "daycare/pay_fees.html", {"fee": fee, "current_month": now().strftime("%B")})

def parent_send_complaint(request):
    if request.method == "POST":
        complaint_text = request.POST.get("complaint")

        if not complaint_text:
            return HttpResponse("Complaint field cannot be empty.")

        try:
            parent_obj = parent.objects.get(id=request.session.get('pid'))  # Fetch logged-in parent
        except parent.DoesNotExist:
            return HttpResponse("Parent not found.")

        # Create a new complaint entry
        complaint.objects.create(
            PARENT=parent_obj,
            complaint=complaint_text,
            complaint_date=now().strftime("%Y-%m-%d"),  # Store current date
            reply="pending",  # Empty initially
            reply_date="pending"
        )

        return HttpResponse("<script>alert('Complaint submitted successfully');window.location='/view_reply_complaint'</script>")

    return render(request, "daycare/parent_send_complaint.html")

def view_reply_complaint(request):
    try:
        parent_obj = parent.objects.get(id=request.session.get('pid'))  # Get logged-in parent
    except parent.DoesNotExist:
        return HttpResponse("Parent not found.")

    # Fetch complaints made by the logged-in parent
    complaints = complaint.objects.filter(PARENT=parent_obj)

    return render(request, "daycare/view_reply_complaint.html", {"complaints": complaints})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

def parent_send_enquiry(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        enquiry_text = request.POST.get("enquiry")

       

        try:
            parent_obj = parent.objects.get(id=request.session.get('pid'))  # Get parent object
            staff_obj = staff.objects.get(id=staff_id)  # Get staff object
        except (parent.DoesNotExist, student.DoesNotExist, staff.DoesNotExist):
            return HttpResponse("Invalid parent, student, or staff.")

        # Save enquiry
        Enquiry.objects.create(
            parent=parent_obj,
            staff=staff_obj,
            enquiry=enquiry_text,
            reply='Pending',
            date=datetime.now().strftime("%Y-%m-%d")  # Store current date
        )

        return HttpResponse("<script>alert('Enquiry Sent Successfully');window.location='/view_reply_enquiry'</script>")

    # Fetch all staff members and students for selection
    staff_members = staff.objects.all()
    students = student.objects.all()  # Assuming parents can choose which child they are inquiring about

    return render(request, "daycare/send_enquiry.html", {"staff_members": staff_members, "students": students})




def view_reply_enquiry(request):
    try:
        parent_obj = parent.objects.get(id=request.session.get('pid'))  # Get logged-in parent
    except parent.DoesNotExist:
        return HttpResponse("Parent not found.")

    # Fetch complaints made by the logged-in parent
    enquiries = Enquiry.objects.filter(parent=parent_obj)

    return render(request, "daycare/view_reply_enquiry.html", {"enquiries": enquiries})



def view_enquiry(request):
    enquiries=Enquiry.objects.filter(staff_id=request.session['sid'])
    return render(request, "staff/view_enquiry.html", {"enquiries": enquiries})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event
from datetime import datetime

def add_event(request):
    if request.method == "POST":
        event_name = request.POST.get("event_name")
        details = request.POST.get("details")
        event_date = request.POST.get("date")

        # Validation: Ensure all fields are filled
        if not event_name or not details or not event_date:
            return HttpResponse("<script>alert('All fields are required!');window.location='/add_event'</script>")

        # Save event
        Event.objects.create(
            event_name=event_name,
            details=details,
            date=event_date
        )

        return HttpResponse("<script>alert('Event Added Successfully');window.location='/add_event'</script>")

    return render(request, "staff/add_event.html")


def view_events(request):
    events = Event.objects.all().order_by('-date')  # Fetch all events sorted by date (latest first)
    return render(request, "daycare/view_events.html", {"events": events})


from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse
from .models import Lesson, student
import datetime
from django.conf import settings

def add_lesson(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")
    
    lessons = Lesson.objects.all()

    if request.method == 'POST':
        lesson_name = request.POST['lesson_name']  # 'lesson_name' instead of 'title'
        details = request.POST['details']  # 'details' instead of 'description'
        subject = request.POST['subject']  # 'subject' as it is, if you need to store it
        date = request.POST['date']  # 'date' from the form
        
        student_id = request.POST.get('student')  # Get the student ID from the form
        student_instance = student.objects.get(id=student_id)  # Get the student object
        
        # Handle file upload
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            photo_path = fs.save(f"videos/{dt}.mp4", uploaded_file)
            photo_url = fs.url(photo_path)

            # Create Lesson object
            lesson = Lesson(
                student=student_instance,  # Associate with the selected student
                lesson_name=lesson_name,
                file=photo_url,  # Store the file path
                details=details,
                date=date
            )
            lesson.save()

    # Get list of students (and teachers, if needed)
    students = student.objects.all()

    return render(request, 'Teacher/add_lesson.html', {'students': students, 'lessons': lessons})



def view_lessons(request):
    lessons=Lesson.objects.all()
    return render(request, 'Daycare/view_lessons.html', { 'lessons': lessons})

# def click_summarize(request,id):
#     a=Lesson.objects.get(id=id)
#     f=a.file
#     if f.endswith('.docx')


#
# def add_photo_video(request):
#     if 'lid' not in request.session:
#         return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")
#
#     if request.method == 'POST':
#         file = request.FILES['select2']
#         date = request.POST['date']
#         d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#
#         fs = FileSystemStorage()
#
#         file_extension = file.name.split('.')[-1].lower()
#
        # data = parent.objects.filter(id=request.session['pid'])
#
#         if data.exists():
#             return HttpResponse("<script>alert('added');window.location='/view_food_menu_new#aa'</script>")
#         else:
#             obj = File()
#             obj.file = path
#             obj.date = date  # Store the file path in the database
#             obj.PARENT_id = request.session['pid']  # Use session data to associate the parent
#             obj.save()
#
#             return HttpResponse("<script>alert('successs');window.location='/view_food_menu_new#aa'</script>")
#
#     # Handle GET request - Render the upload page
#     return render(request, 'Daycare/add_photo_video.html')
#







# def add_photo_video(request):
#     if 'lid' not in request.session:
#         return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")
#
#     if request.method == 'POST':
#         file = request.FILES['select2']
#         date = request.POST['date']
#         # d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#
#         fs = FileSystemStorage()
#         path=fs.save(file.name,file)
#         obj = File()
#         obj.file = path
#         obj.date = date
#         obj.PARENT_id = request.session['pid']
#         obj.save()
#
#
#         fpath="C:\\Users\\prana\\Downloads\\Preschool\\Preschool\\media\\"+ file.name
#
#
#         if file.endswith('.mp4'):
#             doc=veidosumma(fpath)
#         elif file.endswith('.docx'):
#             doc2=exracttext(fpath)
#         else:
#             return HttpResponse("<script>alert('Not Found');window.location='/view_food_menu_new#aa'</script>")
#
#         return HttpResponse("<script>alert('successs');window.location='/view_food_menu_new#aa'</script>")
#
#     return render(request, 'Daycare/add_photo_video.html',{'mp':doc,'doc2':doc2})



import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from .models import File

def add_photo_video(request):
    if 'lid' not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login again');window.location='/'</script>")



    if request.method == 'POST':
        file = request.FILES['select2']
        date = request.POST['date']

        from datetime import datetime
        fname= datetime.now().strftime("%Y%M%d%H%M%S")

        fs = FileSystemStorage()
        path = fs.save(fname+file.name, file)  # Saves the file and returns the relative path
        fpath = fs.path(path)  # Get the full file path

        obj = File()

        obj.file = path
        obj.student = student.objects.get(PARENT__LOGIN_id=request.session['lid'])
        obj.date = date
        obj.PARENT_id = request.session['pid']
        obj.save()

        if file.name.lower().endswith('.mp4'):
            doc = veidosumma(fpath)
            return render(request, 'view result.html', {'mp': doc})

        elif file.name.lower().endswith('.docx'):
            doc2 = exracttext(fpath)
            return render(request, 'view result.html', { 'doc2': doc2})

        else:
            return HttpResponse("<script>alert('Not Found');window.location='/view_food_menu_new#aa'</script>")

        return render(request, 'view result.html', {'mp': doc, 'doc2': doc2})

    return render(request, 'Daycare/add_photo_video.html')


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def download_pdf(request):
    # Prepare the data to be included in the PDF
    mp_summary = request.GET.get('mp', 'No MP4 Video Summary provided.')
    docx_text = request.GET.get('doc2', 'No extracted text from DOCX provided.')

    # Create a response object with content type 'application/pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file_details.pdf"'

    # Prepare the PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create styles for the text
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    body_style = styles['BodyText']

    # Create content (wrapped paragraphs)
    title = Paragraph("Uploaded File Details", title_style)
    mp_paragraph = Paragraph(f"<b>MP4 Video Summary:</b> {mp_summary}", body_style)
    docx_paragraph = Paragraph(f"<b>Extracted Text from DOCX:</b> {docx_text}", body_style)

    # Build the PDF with the content
    elements = [title, mp_paragraph, docx_paragraph]
    doc.build(elements)

    return response





def games(request):
    return render(request,'game.html')


def image_game(request):
    return render(request,'image game.html')




def sudokku_game(request):
    return render(request,'sudokku.html')
