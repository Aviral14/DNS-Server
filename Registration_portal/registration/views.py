from django.shortcuts import render, redirect
from django.contrib import messages
import tld
from .forms import RegistrationForm
from .host_file import records


def register_domain(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            status = check_duplicacy(url=form_obj.url, ip=form_obj.ip)
            if status:
                form_obj.save()
                messages.success(request, "Domain Successfully Registered")
            else:
                messages.error(request, "Given IP Address or Domain already exists")
            return redirect("http://localhost:8000/register/")
        else:
            form = RegistrationForm()
            return render(request, "registeration/register.html", {"form": form})


def check_duplicacy(url, ip):
    pass
