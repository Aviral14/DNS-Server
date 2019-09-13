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
            if (
                form_obj.domain[:7] == "http://"
                or form_obj.domain[:8] == "https://"
                or form_obj.domain[:4] == "www."
            ):
                messages.error(
                    request, "Please Enter the domain in the format specified"
                )
                return redirect("")
            form_obj.user = request.user
            duplicacy = update_records(domain=form_obj.domain, ip=form_obj.ip)
            if not duplicacy:
                form_obj.save()
                messages.success(request, "Domain Successfully Registered")
            else:
                messages.error(request, "Given IP Address or Domain already exists")
            return redirect("register-page")
    else:
        form = RegistrationForm()
        return render(request, "register-page", {"form": form})


def update_records(domain, ip):
    domain_modified = "http://" + domain
    domain_obj = tld.get_tld(domain_modified, as_object=True)
    second_domain = domain_obj.domain
    top_domain = domain_obj.tld
    subdomain = domain_obj.subdomain
    if records.get(top_domain, ""):
        if second_domain in list(records[top_domain].keys()):
            return True
        elif subdomain in list(records[top_domain][second_domain].keys()):
            return True
        elif ip == records[top_domain][second_domain][subdomain]:
            return True
        else:
            records[top_domain].update({second_domain: {subdomain: ip}})
            return False
    else:
        records.update({top_domain: {second_domain: {subdomain: ip}}})
        return False

