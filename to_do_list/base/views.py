from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from.models import Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView # create from and insert data
from django.urls import reverse_lazy # to forth and back on web
from django.contrib.auth.views import LoginView#, LogoutView
from django.views import View
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

# class CustomLogoutView(LogoutView):
#     http_method_names = ['post', 'get']
    # next_page = reverse_lazy('login')  # where to redirect after logout
    # next_page = 'login'
    # def get_success_url(self):
    #     return reverse_lazy('tasks')
    # def get_success_url(self):
    #     success_url = reverse_lazy('login')
    #     print(f"Success URL: {success_url}")
    #     return success_url
    # def get_success_url(request):
        # return redirect('login')

# class CustomLogoutView(LogoutView):
#     http_method_names = ['post', 'get']

#     def get(self, request, *args, **kwargs):
#         self.logout(request)
#         return HttpResponseRedirect(self.get_success_url('login'))

#     def post(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)
    
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login'))

#class based view type listview class
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    # return HttpResponse("hello world")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(tittle__startswith=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html' # by default it gives it model name as prefix and _detail as suffix for template name (other classes also do same)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields = '__all__' #for modelform
    fields = ['tittle', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    # fields = '__all__' #for modelform
    fields = ['tittle', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')