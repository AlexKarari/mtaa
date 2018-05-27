from django.shortcuts import render, redirect
from .models import Profile, Hood, Business, Post, save_user_profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm, NewBusinessForm, NewPostForm, EditProfile, NewSocialForm, NewHoodForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    post = Post.objects.all()
    return render(request, 'all/index.html', {"post": post})


@login_required(login_url='/accounts/login/')
def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_business_name(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html', {"message": message, "searched_businesses": searched_businesses})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all/search.html', {"message": message})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

@login_required(login_url='/accounts/login/')
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('edit')
        
    else:
        return render(request, 'registration/account_activation_invalid.html')


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('homepage')
    else:
        form = NewPostForm()
    return render(request, 'all/post.html', {"form": form})
    

@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    current_user = request.user
    profiles = Profile.objects.filter(user__id__iexact=profile_id)
    profile = Profile.objects.get(user__id__iexact=profile_id)
    all_profile = Profile.objects.all()
    content = {
        "profiles": profiles,
        "profile": profile,
        "user": current_user,
        "profile_id": profile_id,
        "all_profile": all_profile
    }
    return render(request, "all/profile.html", content)


@login_required(login_url='/accounts/login/')
def edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            current_user = request.user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', current_user.username)
    else:
        form = EditProfile()
    return render(request, 'all/editprofile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def business(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewBusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.save()
            return redirect('homepage')
    else:
        form = NewBusinessForm()
    return render(request, 'all/business.html', {"form": form})

@login_required(login_url='/accounts/login/')
def social_ammenities(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewSocialForm(request.POST)
        if form.is_valid():
            social = form.save(commit=False)
            social.user = current_user
            social.save()
            return redirect('homepage')
    else:
        form = NewSocialForm()
    return render(request, 'all/social_ammenities.html', {"form": form})


@login_required(login_url='/accounts/login/')
def neighbourhood(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewHoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = current_user
            hood.save()
            return redirect('homepage')
    else:
        form = NewHoodForm()
    return render(request, 'all/hood.html', {"form": form})


@login_required(login_url='/accounts/login/')
def bizdisplay(request):
    biz = Business.objects.all()
    return render(request, 'all/bizdisplay.html', {"biz": biz})
