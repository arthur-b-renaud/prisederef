from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from prisederef.models import Candidate, Reference


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("login", "").strip()
        password = request.POST.get("password", "").strip()
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Please provide both username and password.")
    
    return render(request, "login.html")


@login_required
def home(request):
    # Get candidates with reference counts
    candidates = (
        Candidate.objects.annotate(num_refs=Count("references"))
        .order_by("name")
    )
    
    # Get the latest 10 references
    latest_references = Reference.objects.select_related(
        'candidate', 'corporation', 'referent'
    ).order_by('-created_at')[:10]
    
    return render(request, "home.html", {
        "candidates": candidates,
        "latest_references": latest_references
    })


def logout_view(request):
    logout(request)
    return redirect("login")
