from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)

class parent(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)


class staff(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)

class student(models.Model):
    student_name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    PARENT = models.ForeignKey(parent, on_delete=models.CASCADE, default=1)



class teacher(models.Model):
    First_name = models.CharField(max_length=100,null=True)
    Last_name = models.CharField(max_length=100,null=True)
    Place = models.CharField(max_length=100,null=True)
    Phone = models.CharField(max_length=10,null=True)  # Limited to 15 characters for better validation
    Email = models.CharField(max_length=100,null=True)  # Ensuring unique email addresses
    Designation = models.CharField(max_length=100,null=True)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)


class assign(models.Model):
    TEACHER = models.ForeignKey(teacher, on_delete=models.CASCADE, default=1)
    date = models.CharField(max_length=100)
    STUDENT=models.ForeignKey(student, on_delete=models.CASCADE,null=True)
    assigned_status = models.CharField(max_length=100)

class attendance(models.Model):
    attendance1 = models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    STUDENT=models.ForeignKey(student, on_delete=models.CASCADE)
    TEACHER=models.ForeignKey(teacher, on_delete=models.CASCADE)



class performance(models.Model):
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE, default=1)
    performance1=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    mark=models.CharField(max_length=100)
    TEACHER=models.ForeignKey(teacher, on_delete=models.CASCADE, default=1)

class rating(models.Model):
    rating = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    PARENT = models.ForeignKey(parent, on_delete=models.CASCADE, default=1)


class feedback(models.Model):
    feedback = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    PARENT = models.ForeignKey(parent, on_delete=models.CASCADE, default=1)


class Activity(models.Model):
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    description = models.CharField(max_length=155)
    date = models.CharField(max_length=155)





class Lesson(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=255)
    file = models.CharField(max_length=2000,null=True)
    details = models.CharField(max_length=1000)  # Changed from TextField to CharField
    date = models.CharField(max_length=100)  # Changed from DateField to CharField

class Work(models.Model):
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    work_description = models.CharField(max_length=1000)  # Changed from TextField to CharField
    date = models.CharField(max_length=100)  # Changed from DateField to CharField

class UploadWork(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    file = models.CharField(max_length=1000)  # Changed from FileField to CharField
    date = models.CharField(max_length=100)  # Changed from DateField to CharField

# Events
class Event(models.Model):
    event_name = models.CharField(max_length=255)
    details = models.CharField(max_length=1000)  # Changed from TextField to CharField
    date = models.CharField(max_length=100)  # Changed from DateField to CharField

# Fees and Payment models
class Fee(models.Model):
    amount = models.CharField(max_length=100)  # Changed from DecimalField to CharField
    student = models.ForeignKey(student, on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,null=True) 

class Payment(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)  # Changed from DecimalField to CharField
    month = models.CharField(max_length=50)
    date = models.CharField(max_length=100)  # Changed from DateField to CharField

# Enquiry model linked with Staff and Student
class Enquiry(models.Model):
    parent = models.ForeignKey(parent, on_delete=models.CASCADE,null=True)
    staff = models.ForeignKey(staff, on_delete=models.CASCADE,null=True)
    enquiry = models.CharField(max_length=1000,null=True)  # Changed from TextField to CharField
    reply = models.CharField(max_length=1000, null=True, blank=True)  # Changed from TextField to CharField
    date = models.CharField(max_length=100)  # Changed from DateField to CharField



# Files uploaded by Student
class File(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    file = models.CharField(max_length=1000)  # Changed from FileField to CharField
    date = models.CharField(max_length=100)  



class complaint(models.Model):
    PARENT = models.ForeignKey(parent, on_delete=models.CASCADE, default=1)
    complaint = models.CharField(max_length=100)
    complaint_date = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    reply_date = models.CharField(max_length=100)























##################################################################################################################33



