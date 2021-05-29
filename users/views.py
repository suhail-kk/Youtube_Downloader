from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .forms import CreateUserForm
from pytube import YouTube
from django.http import HttpResponse


@csrf_protect
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'users/register.html', context)


@csrf_protect
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'users/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# def downloadVideo(request):
#     # downloadVideo(requaest)
#
#     return render(request, 'users/download.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'users/index.html')


def download(request):
    if request.method == 'POST':
        video_url = request.POST['video_url']
        yt = YouTube(video_url)
        thumbnail_url = yt.thumbnail_url
        title = yt.title
        length = yt.length
        desc = yt.description
        view = yt.views
        rating = yt.rating
        age_restricted = yt.age_restricted
        res = render(request, 'users/index.html',
                     {"title": title, "thumbnail_url": thumbnail_url, "video_url": video_url})
        return res
    else:
        res = render(request, 'users/index.html')
        return res


def downloading(request):
    if request.method == 'POST':
        formatRadio = request.POST['formatRadio']
        if formatRadio != "audio":
            qualityRadio = request.POST['qualityRadio']
        video_url_d = request.POST['video_url_d']
        print(formatRadio)
        # print(qualityRadio)
        yt = YouTube(video_url_d)
        print(yt)
        print("Downloading start ....")
        if formatRadio == "audio":
            yt.streams.filter(type=formatRadio).last().download()
        else:
            yt.streams.filter(type=formatRadio, resolution=qualityRadio).first().download()
        print("Downloding completed")
    res = render(request, 'users/index.html', {"msg": "downloading completed"})
    return res
