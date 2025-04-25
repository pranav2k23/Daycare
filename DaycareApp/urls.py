"""Daycare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from DaycareApp import views

urlpatterns = [
    path('',views.log),
    path('change_password',views.change_password),
    path('send_reply/<id>',views.send_reply),
    path('send_replyy/<id>',views.send_replyy),
    path('verified_daycare',views.verified_daycare),
    path('view_and_verify_daycare',views.view_and_verify_daycare),
    path('approve/<id>',views.approve),
    path('reject/<id>',views.reject),
    path('view_complaint',views.view_complaint),
    path('view_feedback',views.view_feedback),
    path('view_parent',views.view_parent),
    path('view_rating',views.view_rating),
    path('view_student',views.view_student),
    path('view_teacher_in_daycare/<id>',views.view_teacher_in_daycare),
    path('login_post',views.login_post),
    path('change_password_post',views.change_password_post),
    path('send_reply_post/<id>',views.send_reply_post),
    path('send_replyy_post/<id>',views.send_replyy_post),
    path('admin_home',views.admin_home),


#--------------------------- daycare ------------------------
    path('add_facility',views.add_facility),
    path('add_fee',views.add_fee),
    path('add_food_menu',views.add_food_menu),
    path('add_meeting',views.add_meeting),
    path('add_teacher',views.add_teacher),
    path('assign_teacher',views.assign_teacher),
    path('edit_facility/<id>',views.edit_facility),
    path('edit_fee/<id>',views.edit_fee),
    path('edit_food_menu',views.edit_food_menu),

    path('edit_teacher/<id>',views.edit_teacher),
    path('Register',views.Register),
    path('manage_profile',views.manage_profile),
    path('view_all_students',views.view_all_students),
    path('view_assign',views.view_assign),
    path('view_attendance/<id>',views.view_attendance),
    path('view_facility',views.view_facility),
    path('view_fee',views.view_fee),
    path('view_food_menu_new',views.view_food_menu_new),
    path('view_meeting',views.view_meeting),
    path('view_payment',views.view_payment),
    path('view_performance/<id>',views.view_performance),
    path('view_daycare_rating',views.view_daycare_rating),
    # path('view_daycare_rating',views.view_daycare_rating),
    path('view_request_from_parent',views.view_request_from_parent),
    path('view_teacher',views.view_teacher),
    path('view_verified_request',views.view_verified_request),
    path('daycare_home',views.daycare_home),
    path('add_facility_post',views.add_facility_post),
    path('add_fee_post',views.add_fee_post),
    path('add_food_menu_post',views.add_food_menu_post),
    path('add_meeting_post',views.add_meeting_post),
    path('add_teacher_post',views.add_teacher_post),
    path('assign_teacher_post',views.assign_teacher_post),
    path('edit_facility_post/<id>',views.edit_facility_post),
    path('Register_post',views.Register_post),
    path('manage_profile_post',views.manage_profile_post),
    path('daycare_change_password',views.daycare_change_password),
    path('daycare_change_password_post',views.daycare_change_password_post),
    path('assignn/<id>/<tid>',views.assignn),
    path('view_teachers/<id>',views.view_teachers),
    path('edit_food_menu_post/<id>',views.edit_food_menu_post),
    path('edit_food_menu/<id>',views.edit_food_menu),
    path('delete_food_menu/<id>',views.delete_food_menu),
    path('edit_fee_post/<id>',views.edit_fee_post),
    path('delete_fee/<id>',views.delete_fee),
    path('delete_facility/<id>',views.delete_facility),
    path('edit_teacher_post/<id>',views.edit_teacher_post),
    path('delete_teacher/<id>',views.delete_teacher),
    path('approve_request/<id>',views.approve_request),
    path('reject_request/<id>',views.reject_request),
    path('approved_request',views.approved_request),
    path('edit_meeting_post/<id>',views.edit_meeting_post),
    path('edit_meeting/<id>', views.edit_meeting),
    path('delete_meeting/<id>',views.delete_meeting),



#--------------------------- teacher ------------------------

    path('view_charges',views.view_charges),
    path('view_all_student',views.view_all_student),
    path('add_attendance1/<id>',views.add_attendance1),
    path('add_attendance_post/<id>',views.add_attendance_post),
    path('view_attendance1/<id>',views.view_attendance1),
    path('edit_attendance/<id>',views.edit_attendance),
    path('edit_attendance_post/<id>',views.edit_attendance_post),
    path('add_performance/<id>',views.add_performance),
    path('add_performance_post/<id>',views.add_performance_post),
    path('view_performance1/<id>',views.view_performance1),
    path('change_password1',views.change_password1),
    path('change_password1_post',views.change_password1_post),
    path('send_notification/<id>',views.send_notification),
    path('send_notification_post/<id>',views.send_notification_post),
    path('view_meeting1',views.view_meeting1),
    path('view_rating1',views.view_rating1),
    path('teacher_home',views.teacher_home),
    path('delete_performance/<id>',views.delete_performance),
    path('edit_performance_post/<id>',views.edit_performance_post),
    path('edit_performance/<id>',views.edit_performance),
    path('delete_attendance/<id>',views.delete_attendance),




#--------------------------- parent ------------------------
    path('and_login',views.and_login),
    path('add_children', views.add_children),
    path('view_children', views.view_children),
    path('edit_children',views.edit_children),
    path('edit_children_post',views.edit_children_post),
    path('delete_children',views.delete_children),
    path('view_nearby_daycare_rating',views.view_nearby_daycare_rating),
    path('view_teacherss',views.view_teacherss),
    path('view_facilities',views.view_facilities),
    path('view_fees',views.view_fees),
    path('view_food_menu',views.view_food_menu),
    path('send_request_to_daycare',views.send_request_to_daycare),
    path('view_request_status',views.view_request_status),
    path('view_class__incharge',views.view_class__incharge),
    path('make_call',views.make_call),
    path('view_notifications',views.view_notifications),
    path('view_atendances',views.view_atendances),
    path('view_performances',views.view_performances),
    path('view_meetings',views.view_meetings),
    path('send_rating',views.send_rating),
    path('android_online_payment',views.android_online_payment),
    path('android_offline_payment',views.android_offline_payment),
    path('send_complaint',views.send_complaint),
    path('view_reply',views.view_reply),
    path('view_feedbacks',views.view_feedbacks),
    path('change_pass',views.change_pass),
    #path('change_pass_post',views.change_pass_post),
    path('register',views.register),
    path('view_ratings',views.view_ratings),
    path('view_profile',views.view_profile),
    path('edit_profiles',views.edit_profiles),
    path('send_feedback',views.send_feedback),
    path('forgot_password',views.forgot_password),
    path('forgot_pass',views.forgot_pass),
    path('forgot_pass_post',views.forgot_pass_post),


    
    path('add_activities',views.add_activities),
    path('view_activities',views.view_activities),
    path('add_activities_post/<id>',views.add_activities_post),
    path('view_student_profile',views.view_student_profile),
    path('add_student',views.add_student),
    path('add_student_post/<id>',views.add_student_post),
    path('add_photo_video',views.add_photo_video),

    path('assign_teacher/<id>',views.assign_teacher),
    path('view_assigned_teacher',views.view_assigned_teacher),
    path('add_lesson', views.add_lesson, name='add_lesson'),
    path('view_assigned_students',views.view_assigned_students),
    path('staff_register',views.staff_register),


    
    path('staff_home',views.staff_home),
    path('view_edit_student_profile',views.view_edit_student_profile),
    path('add_work/<id>',views.add_work),
    path('view_photo_video/<id>',views.view_photo_video),
    path('share_lesson/<id>',views.add_lesson),

    path('view_works',views.view_works),
    path('upload_work/<id>',views.upload_work),
    path('staff_add_fees',views.staff_add_fees),
    path('view_studentfees',views.view_studentfees),
    path('parent_view_fee',views.parent_view_fee),
        path('pay_fees/<id>',views.pay_fees),
    path('parent_send_complaint',views.parent_send_complaint),
    path('view_reply_complaint',views.view_reply_complaint),
    path('parent_send_enquiry',views.parent_send_enquiry),
    path('view_reply_enquiry',views.view_reply_enquiry),
    path('view_enquiry',views.view_enquiry),

    path('add_event', views.add_event, name='add_event'),


    path('view_events', views.view_events, name='view_events'),
    path('view_lessons', views.view_lessons, name='view_lessons'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),




    path('games', views.games, name='games'),
    path('image_game', views.image_game, name='image_game'),
    path('sudokku_game', views.sudokku_game, name='sudokku_game'),

    # path('summarize_video/<int:id>/', views.summarize_video, name='summarize_video'),

]