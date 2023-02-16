from django import forms
# from models import Document


class FileUpload(forms.Form):
    file = forms.FileField()
    # file = Document
