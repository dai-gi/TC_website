from .forms import PostForm, WorkForm, ContactForm
from .models import Post, Work, Category, WorkCategory
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap
import re
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from functools import reduce
from operator import and_
from django.core.paginator import Paginator


class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        paginator = Paginator(post_data, 1)
        page = request.GET.get('page', 1)
        pages = paginator.page(2)

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)   

        return render(request, 'app/index.html', {
            'post_data': post_data,
            'pages':pages,
        })


class MemberView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        work_data = Work.objects.order_by("-id")
        return render(request, 'app/member.html', {
            'post_data': post_data,
            'work_data': work_data,
        })


class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = form = ContactForm(request.POST or None)

        return render(request, 'app/contact.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            if re.search('[ぁ-ん]', message) == None:
                return redirect('thanks')

            subject = 'お問い合わせありがとうございます。'
            content = textwrap.dedent('''
                ※このメールはシステムからの自動返信です。
                
                {name} 様
                
                お問い合わせありがとうございました。
                以下の内容でお問い合わせを受け付けいたしました。
                内容を確認させていただき、ご返信させて頂きますので、少々お待ちください。
                
                --------------------
                ■お名前
                {name}
                
                ■メールアドレス
                {email}
                
                ■メッセージ
                {message}
                --------------------
                ''').format(
                    name=name,
                    email=email,
                    message=message
                )

            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")

            return redirect('thanks')

        return render(request, 'app/contact.html', {
            'form': form
        })


class PostListView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        return render(request, 'app/post_list.html', {
            'post_data': post_data
        })

class PostListMemberView(View):
    def get(self, request, *args, **kwargs):
        post_data_member = Post.objects.order_by("-id")
        return render(request, 'app/post_list_member.html', {
            'post_data_member': post_data_member
        })


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
        })


class PostDetailMemberView(View):
    def get(self, request, *args, **kwargs):
        post_data_member = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail_member.html', {
            'post_data_member': post_data_member
        })


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.text = form.cleaned_data['text']
            post_data.published_date = timezone.now()
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form': form
        })


class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'category': post_data.category,
                'text': post_data.text,
                'image': post_data.image,
            }
        )

        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.text = form.cleaned_data['text']
            post_data.published_date = timezone.now()
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {
            'form': form
        })

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/post_list.html', {
            'post_data': post_data
        })


class CategoryMemberView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data_member = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/post_list_member.html', {
            'post_data_member': post_data_member
        })


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('member')


class WorkListView(View):
    def get(self, request, *args, **kwargs):
        work_data = Work.objects.order_by("-id")
        return render(request, 'app/work_list.html', {
            'work_data': work_data
        })


class WorkDetailView(View):
    def get(self, request, *args, **kwargs):
        work_data = Work.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/work_detail.html', {
            'work_data': work_data
        })


class CreateWorkView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = WorkForm(request.POST or None)

        return render(request, 'app/work_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = WorkForm(request.POST or None)

        if form.is_valid():
            work_data = Work()
            work_data.author = request.user
            work_data.title = form.cleaned_data['title']
            work_category = form.cleaned_data['work_category']
            work_category_data = WorkCategory.objects.get(name=work_category)
            work_data.work_category = work_category_data
            work_data.address = form.cleaned_data['address']
            work_data.text = form.cleaned_data['text']
            work_data.staff = form.cleaned_data['staff']
            work_data.tel = form.cleaned_data['tel']
            work_data.price = form.cleaned_data['price']
            work_data.published_date = timezone.now()
            work_data.save()
            return redirect('work_detail', work_data.id)

        return render(request, 'app/work_form.html', {
            'form': form
        })


class WorkEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        work_data = Work.objects.get(id=self.kwargs['pk'])
        form = WorkForm(
            request.POST or None,
            initial={
                'title': work_data.title,
                'work_category': work_data.work_category,
                'text': work_data.text,
            }
        )

        return render(request, 'app/work_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = WorkForm(request.POST or None)

        if form.is_valid():
            work_data = Work.objects.get(id=self.kwargs['pk'])
            work_data.title = form.cleaned_data['title']
            work_category = form.cleaned_data['work_category']
            work_category_data = WorkCategory.objects.get(name=category)
            work_data.work_category = work_category_data
            work_data.address = form.cleaned_data['address']
            work_data.text = form.cleaned_data['text']
            work_data.staff = form.cleaned_data['staff']
            work_data.tel = form.cleaned_data['tel']
            work_data.price = form.cleaned_data['price']
            work_data.published_date = timezone.now()
            work_data.save()
            return redirect('work_detail', self.kwargs['pk'])

        return render(request, 'app/work_form.html', {
            'form': form
        })


class WorkCategoryView(View):
    def get(self, request, *args, **kwargs):
        work_category_data = WorkCategory.objects.get(name=self.kwargs['work_category'])
        work_data = Work.objects.order_by('-id').filter(work_category=work_category_data)
        return render(request, 'app/work_list.html', {
            'work_data': work_data
        })

class SearchView(View):
    def get(self, request, *args, **kwargs):
        work_data = Work.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', '　'])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(and_, [Q(title__icontains=q) | Q(
                text__icontains=q) for q in query_list])
            work_data = work_data.filter(query)

        return render(request, 'app/work_list.html', {
            'keyword': keyword,
            'work_data': work_data
        })


class WorkDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        work_data = Work.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/work_delete.html', {
            'work_data': work_data
        })

    def post(self, request, *args, **kwargs):
        work_data = Work.objects.get(id=self.kwargs['pk'])
        work_data.delete()
        return redirect('index')
