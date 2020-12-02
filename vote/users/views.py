from django.views.generic import ListView, DetailView, CreateView
from .models import Employee, Department, Like
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordChangeView

from django.shortcuts import get_object_or_404
from django.db.models import Q


class ChangePasswordView(PasswordChangeView):
    success_url = '/'


class AllEmployeeView(ListView):
    """
    Рендерит список всех сотрудников
    """
    model = Employee
    template_name = 'employees/index.html'
    context_object_name = 'all_employees'
    paginate_by = 6

    def get_queryset(self):
        queryset = Employee.objects.filter(
            is_superuser=False).filter(employment=True).order_by('-like_count')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        department = None
        departments = Department.objects.all()
        query = self.request.GET.get('q')
        department_slug = self.kwargs.get('department_slug')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query))
        if department_slug:
            department = get_object_or_404(Department, slug=department_slug)
            queryset = queryset.filter(department=department)
        context = super().get_context_data(object_list=queryset)
        context['department'] = department
        context['departments'] = departments
        return context


class DetailEmployeeView(DetailView):
    model = Employee
    template_name = 'employees/detail.html'


class CreateLikeView(CreateView):
    model = Like
    fields = ['description']
    template_name = 'employees/add_like.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form, **kwarg):
        obj = form.save(commit=False)
        voter = self.request.user
        slug = self.kwargs.get('slug')
        employee = get_object_or_404(Employee, slug=slug)
        like = Like.objects.filter(
            employee=employee,
            one_who_votes=voter.__str__()
        )
        if len(like) < 1:  # каждый может голосовать один раз за каждого
            obj.one_who_votes = str(voter)
            obj.employee = employee
            obj.description = self.request.POST.get('description')
            obj.save()
            count = len(get_object_or_404(Employee, slug=slug).likes.all())
            Employee.objects.filter(slug=slug).update(like_count=count)
            return super(CreateLikeView, self).form_valid(form)
        return HttpResponseRedirect('/')


class AllLikeView(DetailEmployeeView):
    template_name = 'employees/like_list.html'
