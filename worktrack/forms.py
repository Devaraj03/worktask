from django import forms
from django.contrib.auth.models import User
from .models import Work


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'description', 'assigned_to']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Work title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the task (optional)'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

# class WorkForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)

#     class Meta:
#         model = Work
#         fields = ['title', 'description', 'assigned_to']
