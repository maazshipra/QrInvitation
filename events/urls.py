# events/urls.py
from django.urls import path
from .views import create_event ,home, create_guest,upload_guest_list,scan_qr_code,verify_qr_code,update_attendance,add_guest,remove_guest,update_guest,get_guest_list_html,edit,update_event,get_event,remove_event,manage_guest,event_detail,show_guest,show_evnet,manage_event,get_current_event,count_attendance,export_guest_qr_codes,download_all,get_attendance_count, get_messages,login,signup,logout,feedback,feedback_qr,download_qr,feedback_success,feedbacklist

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('home/', home, name='home'),
    # path('generate-qr/<int:event_id>/', generate_qr, name='generate_qr'),
    path('create-guest/', create_guest, name='create_guest'),
    path('upload-guest-list/<int:event_id>/', upload_guest_list, name='upload_guest_list'),
    path('manage_guest/<int:event_id>' ,manage_guest, name='manage_guest'), 
    path('show_guest/<int:event_id>' ,show_guest, name='show_guest'), 
    path('show_event/' ,show_evnet, name='show_evnet'), 
    path('manage_event/<int:event_id>' ,manage_event, name='manage_event'), 
    path('get_current_event/<int:event_id>/', get_current_event, name='get_current_event'),
    path('event_detail/<int:event_id>', event_detail, name='event_detail'),
    path('scan/<int:event_id>', scan_qr_code, name='scan_qr_code'),
    path('scan/verify/<int:event_id>', verify_qr_code, name='verify_qr_code'),
    
    
    path('download_all/<int:event_id>', download_all, name='download_all'),



    path('update_attendance/<int:event_id>/<str:content>/', update_attendance, name='update_attendance'),
    path('count_attendance/<int:event_id>/', count_attendance, name='count_attendance'),
    path('get_attendance_count/<int:event_id>/', get_attendance_count, name='get_attendance_count'),


    path('add_guest/<int:event_id>/', add_guest, name='add_guest'),
    path('remove_guest/<int:event_id>/<int:guest_id>/', remove_guest, name='remove_guest'),
    path('update_guest/<int:event_id>/<int:guest_id>/', update_guest, name='update_guest'),
    path('get_guest_list_html/<int:event_id>/', get_guest_list_html, name='get_guest_list_html'),
    path('edit/<int:event_id>/', edit, name='edit'),


    path('get_event/<int:event_id>/', get_event, name='get_event'),

    
    path('update_event/<int:event_id>/', update_event, name='update_event'),
    path('remove_event/<int:event_id>/', remove_event, name='remove_event'),

    path('export_qr_codes/<int:event_id>/', export_guest_qr_codes, name='export_guest_qr_codes'),

    
    # messages
    path('get_messages/', get_messages, name='get_messages'),


    # account
    path('signup/',signup, name='signup'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),

    # feedback
    path('feedback/<int:event_id>/',feedback, name='feedback'),
    path('feedback_success/',feedback_success, name='feedback_success'),
    path('feedback_qr/<int:event_id>/', feedback_qr, name='feedback_qr'),
    path('download_qr/<int:event_id>/', download_qr, name='download_qr'),
    path('feedbacklist/', feedbacklist, name='feedbacklist'),
    
]



