from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils.translation import gettext as _
from company.forms import CompanyUpdateForm
from company.models import Company

"""
The 4 views down below are generic django class based views
imported above from django.views.generic
"""

class CompanyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Company
    template_name = "company/company_list.html"
    permission_required = ["eshop.manage_companies"]

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data()
        """ 
        the basic object will be object_list
        With generic class based view on the listview and the detailview
        you can supercharge the context to make object available in templates
        'as seen bellow if I use {{available_variable_in_template }} in the templates 
        it will render Hello world 
        """
        context["available_variable_in_template"] = "Hello world"
        return context



class CompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Company
    template_name = "company/company_detail.html"
    permission_required = ["eshop.manage_companies"]

    def get_queryset(self):
        context = super(CompanyDetailView, self).get_queryset()
        print(context.prefetch_related('pictures').query)
        return context.prefetch_related('pictures')

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data()

        """
        as seen above you can pass extra variables to overcha   rge the context
        """
        return context


"""
In the two examples below weither we specify fields
or we can use form_class

"""
class CompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Company
    permission_required = ["eshop.manage_companies"]
    fields = ["rpps", "adeli", "email", "first_name", "last_name", "date_of_birth"]
    template_name = "company/company_create.html"


class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Company
    permission_required = ["eshop.manage_companies"]
    form_class = CompanyUpdateForm
    template_name = "company/company_update.html"



def Company_list_view(request, *args, **kwargs):
    context = {}
    context["object_list"] = Company.objects.all()
    return render(request, "company/company_list.html", context)

def Company_create_view(request, *args, **kwargs):
    context = {}
    form = CompanyUpdateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, _("The form was updated"))
        object = Company.objects.get(slug=kwargs["slug"])
        return redirect(reverse_lazy("company:company-detail", kwargs={"slug": object.slug}))
    context["form"] = CompanyUpdateForm(instance=object)
    return render(request, "company/company_create.html", context)


def Company_detail_view(request, *args, **kwargs):
    context = {}
    context["object"] = Company.objects.get(slug=kwargs["slug"])
    return render(request, "company/company_detail.html", context)


def Company_update_view(request, *args, **kwargs):
    context = {}
    object = Company.objects.get(slug=kwargs["slug"])
    form = CompanyUpdateForm(request.POST or None, instance=object)
    if form.is_valid():
        form.save()
        messages.success(request, _("The form was updated"))
        return redirect(reverse_lazy("company:company-detail", kwargs={"slug": object.slug}))
    context["form"] = CompanyUpdateForm(instance=object)
    return render(request, "company/company_update.html", context)


def icon_library(request, *args, **kwargs):
    context = {}
    return render(request, "admin/icon_library.html", context)
