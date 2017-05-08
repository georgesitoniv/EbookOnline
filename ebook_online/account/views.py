from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from braces.views import AnonymousRequiredMixin, LoginRequiredMixin

from . import models
from . import forms

class LogIn(AnonymousRequiredMixin, FormView):
    template_name = "account/login.html"
    form_class = forms.LoginForm

    def post(self, request):
        form = forms.LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse_lazy("book:index"))
                else:
                    messages.error(request, "Account Disabled")
            else:
                messages.error(request, "Invalid Username or Password")
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class LogOut(LoginRequiredMixin, View):
    def get(self, request):
        """Redirects to the timeline view if accessed via url."""
        logout(request)
        return HttpResponseRedirect(reverse_lazy('account:login'))

    @login_required
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('account:login'))

class Register(AnonymousRequiredMixin, FormView):
    template_name = "account/register.html"
    form_class = forms.UserForm
    
    def post(self, request):
        form = forms.UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            models.UserProfile.objects.create(user=new_user)
            messages.success(request, "You have successfully registered")
        context = {
            'form': form
            }
        return render(request, self.template_name, context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = models.UserProfile
    template_name = "account/profile.html"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page')
        return super(ProfileDetailView, self).get(request, *args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        book_list = context["object"].user.bookshelf.books.all()
        paginator = Paginator(book_list, self.paginate_by)

        try:
            page_obj = paginator.page(self.page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)
        context["page_obj"] = page_obj
        context["is_paginated"] = len(book_list) > self.paginate_by
        return context

class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = "account/edit_profile.html"
    form_class = forms.UserProfileEditForm

    def post(self, request, *args, **kwargs):
        form = forms.UserProfileEditForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = models.UserProfile.objects.get(slug=self.kwargs["slug"]).user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.userprofile.display_image = form.cleaned_data['display_image']
            print(form.cleaned_data['display_image'])
            user.userprofile.save()
            user.save()
            messages.success(request, "You have successfully edited your profile")
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "account/change_password.html"
    form_class = forms.PasswordEditForm

    def post(self, request, *args, **kwargs):
        form = forms.PasswordEditForm(request.POST)
        user = User.objects.get(id=request.user.id)
        if form.is_valid():
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, "Password updated successfuly.")
                messages.success(request, "Please log in again.")
                logout(request)
                return HttpResponseRedirect(reverse_lazy("account:login"))
            else:
                messages.success(request, "Sorry, that is not your old password.")
        context={
            "form": form,
        }
        return render(request, self.template_name, context)
