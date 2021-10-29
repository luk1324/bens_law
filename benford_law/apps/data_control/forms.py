
from django import forms
from django.db.models import fields
from . import models


class UploadForm(forms.ModelForm):

    the_file = forms.FileField(label = 'Add file')

    class Meta:
        model = models.DataSets
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'dataset_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name your DataSet.'}),
            'column_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'What is the name of column in the file?'}),

        }
        fields = "__all__"
