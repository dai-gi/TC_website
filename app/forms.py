from django import forms
from .models import Category, WorkCategory


class PostForm(forms.Form):
    category_data = Category.objects.all()
    category_choice = {}
    for category in category_data:
        category_choice[category] = category

    title = forms.CharField(max_length=30, label='タイトル')
    category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(category_choice.items()))
    text = forms.CharField(label='内容', widget=forms.Textarea())
    image = forms.ImageField(label='イメージ画像', required=False)


class WorkForm(forms.Form):
    work_category_data = WorkCategory.objects.all()
    work_category_choice = {}
    for work_category in work_category_data:
        work_category_choice[work_category] = work_category

    title = forms.CharField(max_length=30, label='タイトル')
    work_category = forms.ChoiceField(label='案件カテゴリ', widget=forms.Select, choices=list(work_category_choice.items()))
    address = forms.CharField(label='内容', max_length=30)
    text = forms.CharField(label='内容', widget=forms.Textarea())
    staff = forms.CharField(label='内容', max_length=30)
    tel = forms.CharField(label='内容', max_length=30)
    price = forms.CharField(label='内容', max_length=30)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label='名前')
    email = forms.EmailField(max_length=30, label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea())
