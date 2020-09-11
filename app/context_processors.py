from .models import Category, WorkCategory

def common(request):
    category_data = Category.objects.all()
    context = {
        'category_data': category_data,
    }
    return context


def work_common(request):
    work_category_data = WorkCategory.objects.all()
    context = {
        'work_category_data': work_category_data,
    }
    return context