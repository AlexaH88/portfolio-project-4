from django.shortcuts import render, redirect, get_object_or_404
from .models import Song
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms


def song_list(request):
    songs = Song.objects.all().order_by('artist')
    return render(request, 'songs/song_list.html', {
        'songs': songs})


def song_detail(request, slug):
    song = Song.objects.get(slug=slug)
    return render(request, 'songs/song_detail.html', {'song': song})


def user_songs(request):
    user_songs = Song.objects.all().filter(author=request.user)
    return render(
        request, 'songs/user_songs.html', {'user_songs': user_songs}
    )


@login_required(login_url="/accounts/login/")
def add_song(request):
    if request.method == 'POST':
        form = forms.SongForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, "Your song has been added!")
            return redirect('songs:song_list')
    else:
        form = forms.SongForm()
    return render(request, 'songs/add_song.html', {'form': form})


@login_required(login_url="/accounts/login/")
def edit_song(request, slug):
    song = Song.objects.get(slug=slug)
    form = forms.SongForm(request.POST, instance=song)
    if form.is_valid():
        form.save()
        messages.success(request, "Your song has been edited!")
        return redirect('songs:user_songs')
    else:
        form = forms.SongForm(instance=song)
        return render(request, 'songs/edit_song.html', {
            'song': song,
            'form': form})


@login_required(login_url="/accounts/login/")
def delete_song(request, slug):
    song = Song.objects.get(slug=slug)
    song.delete()
    messages.success(request, "Your song has been deleted!")
    return redirect('songs:user_songs')
