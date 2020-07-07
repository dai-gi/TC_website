from django import forms
# from .models import Work

class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    text = forms.CharField(label='内容', widget=forms.Textarea())


class WorkForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    address = forms.CharField(label='内容', max_length=30)
    text = forms.CharField(label='内容', widget=forms.Textarea())
    staff = forms.CharField(label='内容', max_length=30)
    tel = forms.CharField(label='内容', max_length=30)
    price = forms.CharField(label='内容', max_length=30)
