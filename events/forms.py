# events/forms.py
from django import forms
from .models import Event, Guest,Feedback
from django.forms import DateInput
from datetime import date



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date','location']

    def __init__(self,*args, **kwargs):
            super().__init__(*args,**kwargs)            
            self.fields['name'].widget.attrs.update(
                {
                     
                'class': 'form-control',              
            
                })
            self.fields['date'].widget = DateInput(attrs={'type': 'date'})
            self.fields['date'].widget.attrs.update(
                {
                
                'class': 'form-control',
                 'min': date.today(),
                
            
                })
            self.fields['location'].widget.attrs.update(
                            {
                            'class': 'form-control',
                            
                        
                            })        

    

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['event', 'name']



class GuestListUploadForm(forms.Form):
    csv_file = forms.FileField()

    def __init__(self,*args, **kwargs):
            super().__init__(*args,**kwargs)     
                   
            self.fields['csv_file'].widget.attrs.update(
                {
                'class': 'form-control',              
            
                })



class QRCodeForm(forms.Form):
    qr_code = forms.CharField(max_length=255)
    event_id = forms.IntegerField()


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']

    def __init__(self,*args, **kwargs):
            super().__init__(*args,**kwargs)   
                
            self.fields['feedback'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,  
        })