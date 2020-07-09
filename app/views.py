from .forms import PostForm, WorkForm
from app.models import Post, Work
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from functools import reduce
from operator import and_


class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        work_data = Work.objects.order_by("-id")
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'work_data': work_data
        })


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data': post_data
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
            post_data.text = form.cleaned_data['text']
            post_data.published_date = timezone.now()
            if request.FILES:
                post_data.image = request.FILES.get('image') 
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {
            'form': form
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
        return redirect('index')


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