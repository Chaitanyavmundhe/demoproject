from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import UploadedFile


# ─────────────────────────────────────────────
# Login View
# ─────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to find user by email first
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'portal/login.html')


# ─────────────────────────────────────────────
# Logout View
# ─────────────────────────────────────────────

def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────
# Register View
# ─────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password')
        password2  = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'portal/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'portal/register.html')

        User.objects.create_user(
            username=email,   # ← use email as username (must be set)
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'portal/register.html')

# ─────────────────────────────────────────────
# Home / Search View
# ─────────────────────────────────────────────

def home_view(request):
    search_query    = request.GET.get('search', '').strip()
    filter_category = request.GET.get('filter_category', '').strip()

    files = UploadedFile.objects.all().order_by('-uploaded_at')

    if search_query:
        files = files.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if filter_category:
        files = files.filter(category=filter_category)

    return render(request, 'portal/search.html', {'files': files})


# ─────────────────────────────────────────────
# Upload View
# ─────────────────────────────────────────────

@login_required(login_url='login')
def upload_view(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category    = request.POST.get('category')
        semester    = request.POST.get('semester')
        file        = request.FILES.get('file')

        if not file:
            messages.error(request, 'Please select a file to upload.')
            return render(request, 'portal/upload.html')

        UploadedFile.objects.create(
            title=title,
            description=description,
            category=category,
            semester=semester,
            file=file,
            uploaded_by=request.user,
        )
        messages.success(request, f'"{title}" uploaded successfully!')
        return redirect('home')

    return render(request, 'portal/upload.html')