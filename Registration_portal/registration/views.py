import tld
import json
import socket
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

HOST = "127.0.0.1"
PORT = 8080


@login_required
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
                return redirect("register-page")
            form_obj.user = request.user
            duplicacy, records = update_records(domain=form_obj.domain, ip=form_obj.ip)
            if not duplicacy:
                status = send_to_dns(domain=form_obj.domain, ip=form_obj.ip)
                if status == "Success":
                    form_obj.save()
                    with open("registration/host_file.json", "w") as host_file:
                        json.dump(records, host_file)
                    messages.success(request, "Domain Successfully Registered")
                else:
                    messages.success(
                        request,
                        "Can't Connect to DNS Server Right Now! Please Try Again Later.",
                    )
            else:
                if records == "Error":
                    messages.error(request, "Enter a valid Domain Name!")
                else:
                    messages.error(request, "Given Domain Name already exists")
            return redirect("register-page")
        else:
            messages.error(
                request, "Please Enter all the information in the correct format!"
            )
            return redirect("register-page")

    else:
        form = RegistrationForm()
        return render(request, "registration/register-page.html", {"form": form})


def update_records(domain, ip):
    with open("registration/host_file.json") as file_obj:
        records = json.loads(file_obj.read())
    domain_modified = "http://" + domain
    try:
        domain_obj = tld.get_tld(domain_modified, as_object=True)
        second_domain = domain_obj.domain
        top_domain = domain_obj.tld
        subdomain = domain_obj.subdomain
    except:
        return True, "Error"

    if records.get(top_domain, ""):
        if second_domain in list(records[top_domain].keys()):
            if subdomain in list(records[top_domain][second_domain].keys()):
                return True, "Duplicate"
            else:
                records[top_domain][second_domain].update({subdomain: ip})
                return False, records

        else:
            records[top_domain].update({second_domain: {subdomain: ip}})
            return False, records
    else:
        records.update({top_domain: {second_domain: {subdomain: ip}}})
        return False, records


def send_to_dns(domain, ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        try:
            socket_obj.connect((HOST, PORT))
            socket_obj.send(f"{domain},{ip}".encode())
            return "Success"
        except:
            return "Failure"


def signup(request):
    return redirect("account-login")

