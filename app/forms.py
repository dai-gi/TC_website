from django import forms
# from .models import Post

class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    text = forms.CharField(label='内容', widget=forms.Textarea())

    # class Meta:
    #     model = Post
    #     fields = '__all__'
    #     widgets = {
    #         'created_at': forms.SelectDateWidget
    #     }