from django import forms
from .models import *
from account.forms import FormSettings
from datetime import datetime


class VoterForm(FormSettings):
    ACADEMIC_LEVEL_CHOICES = [(str(i), f'Level {i}') for i in range(1, 6)]

    class Meta:
        model = Voter
        fields = ['phone', 'photo', 'date_of_birth', 'address', 'gender', 'department', 'academic_level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo'].required = True
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].required = True
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
        self.fields['address'].required = True
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].required = True
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].required = True
        self.fields['academic_level'].widget.attrs.update({'class': 'form-control'})
        self.fields['academic_level'].choices = self.ACADEMIC_LEVEL_CHOICES
        self.fields['academic_level'].required = True
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].required = True

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        if date_of_birth:
            # Check if date is in the past
            if date_of_birth > datetime.now().date():
                self.add_error('date_of_birth', 'Date of birth cannot be in the future')
        return cleaned_data


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote']


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo']
