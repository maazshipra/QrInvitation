from django.shortcuts import render, redirect, get_object_or_404, HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from .forms import EventForm, GuestForm, GuestListUploadForm, QRCodeForm,FeedbackForm
import qrcode
from firebase import firebase  # Use an appropriate Firebase library
from .models import Event, Guest,Attendance,EventFeedbaackQr
import tempfile
import os
import csv
from io import TextIOWrapper
from io import BytesIO
from django.core.files.base import ContentFile
import pyrebase
import datetime
import uuid 
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.core.files.base import ContentFile
import openpyxl
from openpyxl import Workbook
import io
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
import qrcode
from PIL import Image
from openpyxl.utils import get_column_letter
import zipfile
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import base64








def signup(request):


    if request.method == 'POST':

        username = request.POST.get('signup_username')
        name = request.POST.get('signup_name')
        # mobile = request.POST.get('signup_mobile')
        email = request.POST.get('signup_email')
        password = request.POST.get('signup_pass')
        

        if User.objects.filter(username=username).exists():
                    messages.info(request, ' Username already exists')
                    print('username taken')
                    return redirect('signup')

        elif User.objects.filter(email=email).exists():
                    messages.info(request, ' Email already exists')
                    return redirect('signup')
        else:
                    
                    user = User.objects.create_user(username=username,first_name=name, email=email, password = password)
                    user.save();
                    messages.success(request, "User Created successfully.")
                    print('user created')
                    return redirect('login')

    else:
        return render(request, 'signup.html')



def login(request):


    if request.method == 'POST':

        username = request.POST['signin_name']
        password = request.POST['signin_pass']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Log In successfully.")
            return redirect('home')
        else:
            messages.info(request, 'Invaild Username and Password')
            return redirect('login')
    else:
        return render(request, 'login.html')




def logout(request):

    auth.logout(request)
    messages.success(request, "Log Out successfully.")
    return redirect('login')




# message
def get_messages(request):
    message_list = []
    for message in messages.get_messages(request):
        message_list.append({
            'message': message.message,
            'tag': message.tags,
        })

    return JsonResponse({'messages': message_list})

# def create_event(request):
#     if request.method == 'POST':
#         event_form = EventForm(request.POST)
#         #if event_form.is_valid():
#         event = event_form.save()
#         #return redirect('generate_qr', event_id=event.id)
#         return redirect('create_guest')
#     else:
#         event_form = EventForm()
#     return render(request, 'create_event.html', {'event_form': event_form})
@login_required(login_url="login")
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.user = request.user
            event = event_form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('upload_guest_list', event_id=event.id)
    else:
        event_form = EventForm()
    return render(request, 'create_event.html', {'event_form': event_form,})


# not in use for now
# def generate_qr(request, event_id):
#     event = Event.objects.get(id=event_id)
#     guests = Guest.objects.filter(event=event)

#     for guest in guests:
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(guest.name)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         # Upload the QR code to Firebase
#         firebase_db = firebase.FirebaseApplication('my-application-f56a5.appspot.com', None)
#         result = firebase_db.post('/qrcodes', {'qr_code': img.get_image()})
#         guest.qr_code = result['name']
#         guest.save()

#     messages.success(request, 'QR codes generated and uploaded to Firebase successfully!')
#     return redirect('event_list')

@login_required(login_url="login")
def home(request):
    

    return render(request, 'home.html',)


# def create_guest(request):
#     if request.method == 'POST':
#         guest_form = GuestForm(request.POST)
#         if guest_form.is_valid():
#             guest_form.save()
#             messages.success(request, 'Guest created successfully!')
#             return redirect('create_event')  # Redirect to the event creation page
#     else:
#         guest_form = GuestForm()
#     return render(request, 'create_guest.html', {'guest_form': guest_form})


@login_required(login_url="login")
def create_guest(request):
    if request.method == 'POST':
        guest_form = GuestForm(request.POST)
        if guest_form.is_valid():
            guest = guest_form.save(commit=False)
            guest.user = request.user
            guest_form.save()
            messages.success(request, 'Guest created successfully!')
            return redirect('create_event')  # Redirect to the event creation page
    else:
        guest_form = GuestForm()
    return render(request, 'create_guest.html', {'guest_form': guest_form})


# def upload_guest_list(request, event_id):
#     event = Event.objects.get(id=event_id)
#     if request.method == 'POST':
#         guest_list_upload_form = GuestListUploadForm(request.POST, request.FILES)
#         if guest_list_upload_form.is_valid():
#             csv_file = request.FILES['csv_file']
#             Guest.create_from_csv(event, csv_file)
#             messages.success(request, 'Guest list uploaded successfully!')
#             return redirect('create_event')
#     else:
#         guest_list_upload_form = GuestListUploadForm()
#     return render(request, 'upload_guest_list.html', {'event': event, 'guest_list_upload_form': guest_list_upload_form})


# working without unique
# def upload_guest_list(request, event_id):
#     event = Event.objects.get(id=event_id)
#     event_name = Event.objects.get(id=event_id).name
    
#     guest_list_upload_form = GuestListUploadForm()
#     if request.method == 'POST':
#         form = GuestListUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Process the uploaded CSV file
#             csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
#             csv_reader = csv.reader(csv_file)
#             for row in csv_reader:
#                 if row:
#                     # Create a QR code for each row in the CSV
#                     data = row[0]
#                     qr = qrcode.QRCode(
#                         version=1,
#                         error_correction=qrcode.constants.ERROR_CORRECT_L,
#                         box_size=10,
#                         border=4,
#                     )
#                     qr.add_data(data)
#                     qr.make(fit=True)
#                     qr_img = qr.make_image(fill_color="black", back_color="white")
                    

#                     # Save QR code data to the database
#                     qr_code_data = Guest(event=event,data=data)
#                     qr_code_data.save()


#                      # Save QR code image to the database
#                     img_io = BytesIO()
#                     qr_img.save(img_io, format='PNG')
#                     qr_code_data.qr_code.save(f'qr_code_{qr_code_data.id}.png', ContentFile(img_io.getvalue()))
                
#     else:
#         guest_list_upload_form = GuestListUploadForm()
#     return render(request, 'upload_guest_list.html', {'event': event, 'guest_list_upload_form': guest_list_upload_form, 'event_name':event_name})
@login_required(login_url="login")
def upload_guest_list(request, event_id):
    event = Event.objects.get(id=event_id)
    event_name = Event.objects.get(id=event_id).name
    guest_name = Guest.objects.filter(event_id=event_id).all
    
    
    
    guest_list_upload_form = GuestListUploadForm()
    if request.method == 'POST':
        form = GuestListUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            # Process the uploaded CSV file
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row:

                    guest_name = row[0]
                    # Create a unique identifier for each guest (e.g., using UUID)
                    guest_id = str(uuid.uuid4())

                    # Combine guest Name and guest ID to create a unique data for each QR code
                    
                    
                    data = f'{guest_name}-{guest_id}'

                    # data = f'{event_id}-{guest_id}'

                    # Create a QR code for each row in the CSV
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(data)
                    qr.make(fit=True)
                    qr_img = qr.make_image(fill_color="black", back_color="white")
                    
                    # Save QR code data to the database
                    #upload_csv = form.save(commit=False)
                   
                    qr_code_data = Guest(event=event, name=guest_name,qr_data=data) 
                    qr_code_data.user = request.user
                    qr_code_data.save()

                    # Save QR code image to the database
                    img_io = BytesIO()
                    qr_img.save(img_io, format='PNG')
                    qr_code_data.qr_code.save(f'qr_code_{qr_code_data.id}.png', ContentFile(img_io.getvalue()))
            messages.success(request, "CSV File Uploaded successfully.")
            return redirect('show_guest' ,event_id)
                    
                
    else:
        guest_list_upload_form = GuestListUploadForm()
    return render(request, 'upload_guest_list.html', {'event': event, 'guest_list_upload_form': guest_list_upload_form, 'event_name': event_name,'guest_name':guest_name,})


# addind , removing ,update guest 
@login_required(login_url="login")
def add_guest(request, event_id):
    if request.method == 'POST':
        
        event = get_object_or_404(Event,id=event_id,user=request.user)
        guest_name = request.POST.get('guest_name')
        guest_id = str(uuid.uuid4())


        data = f'{guest_name}-{guest_id}'

        # data = f'{event_id}-{guest_id}'

        # Create a QR code for each row in the CSV
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code data to the database
        qr_code_data = Guest(event=event, name=guest_name,qr_data=data)
        
        qr_code_data.user = request.user
        qr_code_data.save()

        # Save QR code image to the database
        img_io = BytesIO()
        qr_img.save(img_io, format='PNG')
        qr_code_data.qr_code.save(f'qr_code_{qr_code_data.id}.png', ContentFile(img_io.getvalue()))
        messages.success(request, "Guest Updated successfully.")
        return redirect(request.META['HTTP_REFERER'])




        # if guest_name:
        #     new_guest = Guest(event_id=event_id, name=guest_name, qr_data=data)
        #     new_guest.save()

    return HttpResponse(get_guest_list_html(event_id))

#@login_required(login_url="login")
def remove_guest(request, event_id, guest_id,):
    try:
        
        #guest = get_object_or_404(Guest, id=guest_id, event_id=event_id,user=request.user)
        guest = Guest.objects.filter(id=guest_id, event_id=event_id,user=request.user)
        
        guest.delete()
        
        messages.success(request, "Guest Deleted successfully.")
    except Guest.DoesNotExist:

        messages.error(request, "Guest Not Found")
    

    
    
    return HttpResponse(get_guest_list_html(event_id,user=request.user))

@login_required(login_url="login")
def update_guest(request, event_id, guest_id):
    if request.method == 'POST':
        new_guest_name = request.POST.get('new_guest_name')
        if new_guest_name:
            try:
                guest = Guest.objects.get(id=guest_id, event_id=event_id,user=request.user)
                guest.name = new_guest_name

                # Delete the previous QR code file
                # if guest.qr_code:
                #     os.remove(guest.qr_code.path)

                # Regenerate QR code with updated data
                new_qr_data = f'{new_guest_name}-{str(uuid.uuid4())}'
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(new_qr_data)
                qr.make(fit=True)
                new_qr_img = qr.make_image(fill_color="black", back_color="white")

                # Save updated QR code data to the database
                guest.qr_data = new_qr_data
                guest.save()

                # Save updated QR code image to the database
                img_io = BytesIO()
                new_qr_img.save(img_io, format='PNG')
                guest.qr_code.save(f'qr_code_{guest.id}.png', ContentFile(img_io.getvalue()))

            except Guest.DoesNotExist:
                pass

    return HttpResponse(get_guest_list_html(event_id))
@login_required(login_url="login")
def edit(request, event_id):

    return HttpResponse(get_guest_list_html(event_id))


@login_required(login_url="login")
def get_guest_list_html(request,event_id):
    guest_list = Guest.objects.filter(event_id=event_id, user=request.user)
    return render_to_string('guest_list_partial.html', {'guest_list': guest_list})


# show guest
@login_required(login_url="login")
def show_guest(request, event_id):
   
    event =  get_object_or_404(Event, id=event_id, user=request.user)
    guest = Guest.objects.filter(event_id=event_id,user=request.user)
    guest_count = Guest.objects.filter(event_id=event_id).count()
   
    return render(request, 'show_guest.html',{'event':event,'guest':guest,'media_url':settings.MEDIA_URL,'guest_count':guest_count})

# download qr code
# def download_qr(request, event_id, guest_id):
#     guest = Guest.objects.get(id=guest_id)
#     qr_code_path = guest.qr_code.path
#     with open(qr_code_path, 'rb') as file:
#         response = HttpResponse(file.read(), content_type='image/png')
#         response['Content-Disposition'] = f'attachment; filename="{guest.name}_QRCode.png"'
#     return response
@login_required(login_url="login")
def download_all(request, event_id):
     
    event = get_object_or_404(Event, id=event_id, user=request.user)
    guests = Guest.objects.filter(event_id=event_id,user=request.user)

    # Create a BytesIO buffer to store the zip file
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for guest in guests:
            # Get the actual file path from the ImageFieldFile object
            qr_code_path = guest.qr_code.path
            zip_file.write(qr_code_path, f"{guest.name}_QRCode.png")

    # Close the buffer for writing and set the appropriate headers for the response
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_QR_Codes.zip"'

    return response
# show event
@login_required(login_url="login")
def show_evnet(request, ):
    
    event = Event.objects.filter(user=request.user)
    #event = Event.objects.all()
    event_count = event.count()


    
    return render(request, 'show_event.html',{'events':event,'event_count':event_count})

# manage_guest
@login_required(login_url="login")
def manage_guest(request, event_id):

    event = get_object_or_404(Event, id=event_id, user=request.user)
    guest = Guest.objects.filter(event_id=event_id,user=request.user).all
   
    guest_list_upload_form = GuestListUploadForm()
    
    return render(request, 'manage_guest.html',{'event':event,'guest':guest,'media_url':settings.MEDIA_URL,'guest_list_upload_form':guest_list_upload_form})

def manage_event(request,event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    

    return render(request, 'manage_event.html',{'event':event})


# update, delete event
@login_required(login_url="login")
def get_event(request, event_id):
    event = get_object_or_404(Event, id=event_id,user=request.user)
    # guests = get_object_or_404(Guest,event=event,user=request.user)
    guest = Guest.objects.filter(event_id=event_id, user=request.user)
    return render(request, 'guest_list_partial.html', {'guest': guest,'media_url':settings.MEDIA_URL})



@login_required(login_url="login")
def update_event(request, event_id):
    if request.method == 'POST':
        new_event_name = request.POST.get('new_event_name')
        if new_event_name:
            event = get_object_or_404(Event, id=event_id, user=request.user)
            event.name = new_event_name
            event.save()
        messages.success(request, "Name Changed successfully.")
    return JsonResponse({'success': True})

@login_required(login_url="login")
def remove_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id, user=request.user)
        event.delete()
        messages.success(request, "Event Deleted successfully.")
        return JsonResponse({'success': True})
    except Event.DoesNotExist:
        messages.error(request, "Event Not Found")
        return JsonResponse({'success': False})
    
@login_required(login_url="login")
def get_current_event(request, event_id):
    event = get_object_or_404(Event, id=event_id,user=request.user)
    return JsonResponse({'id': event.id})



# verify
@login_required(login_url="login")
def scan_qr_code(request,event_id):

    # event = Event.objects.get(id=event_id);

    event = get_object_or_404(Event, id=event_id,user=request.user)
    attendance_count = Attendance.objects.filter(event=event).count()
    return render(request, 'qrcode_attendance/scan_qr_code.html',{'event':event,'attendance_count':attendance_count})


# def verify_qr_code(request,event_id):
   
#     event = Event.objects.get(id=event_id)
#     if request.method == 'POST':
#         form = QRCodeForm(request.POST)
#         if form.is_valid():
#             qr_code = form.cleaned_data['qr_code']
#             event_id = form.cleaned_data['event_id']

#             # Verify if the QR code corresponds to a guest in the specified event
#             guest = get_object_or_404(Guest, qr_code=qr_code, event_id=event_id)

#             # Check if the guest has already been marked as attended for the event
#             if Attendance.objects.filter(event_id=event_id, guest=guest).exists():
#                 return JsonResponse({'status': 'error', 'message': 'Guest already marked as attended for this event.'})

#             # Mark the guest as attended for the event
#             Attendance.objects.create(event_id=event_id, guest=guest)
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid QR Code or Event'})
#     else:
#         form = QRCodeForm()

#     # guest = Guest.objects.get()
#     return render(request, 'qrcode_attendance/event_detail.html',{'event':event})


@login_required(login_url="login")
def verify_qr_code(request,event_id):
   
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        print(qr_code_data)
        
        # Verify QR code data here
        try:
            qr_code = Guest.objects.get(data=qr_code_data)
            
            if qr_code.is_valid():
                # ... handle valid QR code ...
                response_data = {'valid': True}
            else:
                # ... handle invalid QR code ...
                response_data = {'valid': False}
                
        except Guest.DoesNotExist:
            # ... handle non-existent QR code ...
            response_data = {'valid': False}
            
        return JsonResponse(response_data)
    
    else:
        return JsonResponse({'error': 'Invalid request method'})
    # guest = Guest.objects.get()
    # return render(request, 'qrcode_attendance/event_detail.html',{'event':event})


@login_required(login_url="login")
def event_detail(request,event_id ):
    event = get_object_or_404(Event, id=event_id, user=request.user)

    return render(request, 'event_detail.html',{'event':event})




# def update_attendance(request, content):
#     print(content)
#     guest = get_object_or_404(Guest, qr_data=content)
#     print(guest)
#     event = guest.event
#     print(event)
#     # Check if the guest is already marked as attended for the event
#     if not Attendance.objects.filter(event=event, guest=guest).exists():
#         print("data pass")
#         # Mark attendance
#         attendance = Attendance(event=event, guest=guest)
#         attendance.save()
#         print("Attendance marked successfully.")
#         return HttpResponse("Attendance marked successfully.")
#     else:
#         return HttpResponse("Attendance already marked.")

@login_required(login_url="login")
def update_attendance(request, event_id, content):
    
    guest = get_object_or_404(Guest, qr_data=content,user=request.user)
    
    event = guest.event
    

    # Check if the event ID matches the actual event ID of the guest
    if event.id == event_id:
        # Check if the guest is already marked as attended for the event
        if not Attendance.objects.filter(event=event, guest=guest).exists():
            print("data pass")
            # Mark attendance
            attendance = Attendance(event=event, guest=guest,attended=True)
            
            attendance.user = request.user
            attendance.save()
            print("Attendance marked successfully.")
            messages.success(request, "Attendance marked successfully.")
            return HttpResponse("Attendance marked successfully.")
        else:
            messages.info(request, "Attendance already marked.")
            return HttpResponse("Attendance already marked.")
    else:
        messages.error(request, "Invalid QR Code")
        return HttpResponse("Incorrect event ID.")
    
    
@login_required(login_url="login")
def count_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id,user=request.user)
    attendance = Attendance.objects.filter(event=event,user=request.user)
    
    # List of attendees
    attendees = attendance.filter(attended=True)

    # List of non-attendees
    non_attendees = attendance.filter(attended=False)

    # Guests who have not been marked as attended
    remaining_guests = Guest.objects.filter(event=event).exclude(attendance__attended=True)

    attendance_count = attendance.count()

    return render(request, 'qrcode_attendance/attendance.html', {
        'attendance_count': attendance_count,
        'event': event,
        'attendance': attendance,
        'attendees': attendees,
        'non_attendees': non_attendees,
        'remaining_guests': remaining_guests,
        
    })

@login_required(login_url="login")
def get_attendance_count(request, event_id):
    event = get_object_or_404(Event, id=event_id,user=request.user)
    attendance_counts = Attendance.objects.filter(event=event, attended=True,user=request.user).count()
    

    # Ensure that the response is a valid JSON object
    response_data = {'attendance_counts': attendance_counts}
    return JsonResponse(response_data)

@login_required(login_url="login")
def export_guest_qr_codes(request, event_id):
    # Retrieve guest data from the database for a specific event
    guests = Guest.objects.filter(event_id=event_id)

    # Create a DataFrame to store guest data
    guest_data = {'Name': [], 'QR Code Data': []}

    for guest in guests:
        # Add guest data to the DataFrame
        guest_data['Name'].append(guest.name)
        guest_data['QR Code Data'].append(guest.qr_data)

    # Create a DataFrame from the guest data
    df_guests = pd.DataFrame(guest_data)

    # Create a BytesIO object to store the Excel file
    excel_file = BytesIO()

    # Create a QR code image for each guest and save it to the BytesIO object
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df_guests.to_excel(writer, index=False, sheet_name='Guests')

        worksheet = writer.sheets['Guests']
        for index, qr_data in enumerate(guest_data['QR Code Data']):
            img_io = BytesIO()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(img_io, format='PNG')

            # Resize the QR code image if needed
            img = Image.open(img_io)
            img.thumbnail((50, 50))
            img_io_resized = BytesIO()
            img.save(img_io_resized, format='PNG')

            # Add the QR code image to the Excel file
            worksheet.insert_image(index + 1, 2, f'qr_code_{index + 1}.png', {'image_data': img_io_resized.getvalue()})

    # Set response headers for Excel file download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=guest_qr_codes_{event_id}.xlsx'
    response.write(excel_file.getvalue())

    return response

def feedback(request,event_id):

    event = get_object_or_404(Event, id=event_id,)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            feedback_instance.event = event
            feedback_instance.save()
            # You can add a success message if needed

            return redirect('feedback_success')  # Redirect to a success page
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form, 'event': event})

def feedback_success(request):

    return render(request, 'feedback/feedback_success.html')
  
def feedback_qr(request, event_id):

    event = get_object_or_404(Event, id=event_id, user=request.user )
    # Construct the feedback URL with the event_id or any other identifier
    feedback_url = f"http://192.168.0.104:8000/feedback/{event_id}/"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(feedback_url)
    qr.make(fit=True)

    # Create an image from the QR code data
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image or serve it directly in the response
    img_buffer = BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)

    # img_url = f"data:image/png;base64,{base64.b64encode(img_buffer.getvalue()).decode()}"
    qr_code_image, created = EventFeedbaackQr.objects.get_or_create(event=event)
    qr_code_image.image.save(f'qrcode_{event_id}.png', ContentFile(img_buffer.read()), save=True)

    return render(request, 'feedback/feedback_qr.html', {'qr_code_image': qr_code_image,'event':event})


def download_qr(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user )
    img_path = f"media/feedback_qrcodes/qrcode_{event_id}.png"
    with open(img_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename=feedback_qr_{event.name}.png'
    return response


def feedbacklist(request):

    
    event = Event.objects.get(user=request.user)    
    events_with_qr = EventFeedbaackQr.objects.filter(event=event).all()

    

    return render(request, 'feedback/feedbacklist.html',{'events_with_qr':events_with_qr,})