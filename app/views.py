from app.models import Post, Work
from django.views.generic import View
from django.shortcuts import render

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        work_data = Work.objects.order_by("-id")
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'work_data': work_data
        })

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

