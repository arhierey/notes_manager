from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.forms import modelform_factory

from .forms import SignUpForm
from .models import Note


def main_page(request):
    username = request.user.username
    user = User.objects.get(username=username)
    notes_set = Note.objects.filter(user_id=user)
    return render(request, 'main.html', context={'notes': notes_set})


def first_page(request):
    return render(request, 'first_page.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def new_note_page(request):
    return render(request, 'add_note_page.html')


def add_note(request):
    header = request.POST['header']
    content = request.POST['content']
    note_type = request.POST['type']
    username = request.user.username
    user = User.objects.get(username=username)

    new_note = Note()
    new_note.user_id = user
    new_note.header = header
    new_note.content = content
    new_note.type = note_type
    new_note.save()

    return redirect('profile')


def edit_note(request):
    NoteForm = modelform_factory(Note, exclude=('user_id', 'date'))

    if request.method == 'POST':
        note = Note.objects.get(uuid=request.POST['note'])
        form = NoteForm(instance=note)
        if form.is_valid():
            form.save()
    else:
        form = NoteForm()

    return render(request, 'edit_note_page.html', {'form': form, 'note': request.POST['note']})


def save_edited_note(request):
    note = Note.objects.get(uuid=request.POST['uuid'])
    note.header = request.POST['header']
    note.content = request.POST['content']
    note.type = request.POST['type']

    if request.POST['favorite'] == 'on':
        note.favorite = True

    note.save()

    return redirect('profile')


def go_to_note(request):
    note_id = request.POST['note_id']

    return redirect('/' + note_id)


def note_view(request, note_id):
    note = Note.objects.get(uuid=note_id)
    context = {'header': note.header,
               'content': note.content,
               }

    return render(request, 'note.html', context)


def back_to_main(request, note_id):
    return redirect('profile')


def delete_note(request):
    note_id = request.POST['note_id']

    note_to_delete = Note.objects.get(uuid=note_id)
    note_to_delete.delete()

    return redirect('profile')


def filter_it(request):
    username = request.user.username
    user = User.objects.get(username=username)
    notes_set = Note.objects.filter(user_id=user)

    type_keys_out = ['RF', 'TD', 'NT', 'MM', 'OT']
    for key, value in request.POST.items():
        if key == 'header':
            if value:
                notes_set = notes_set.filter(header__icontains=value)
        elif key == 'start-date':
            if value:
                notes_set = notes_set.filter(date__gte=value)
        elif key == 'end-date':
            if value:
                notes_set = notes_set.filter(date__lte=value)
        elif key in ['RF', 'TD', 'NT', 'MM', 'OT']:
            type_keys_out.remove(value)
        elif key == 'fav':
            if value == 'on':
                notes_set = notes_set.filter(favorite=True)
            else:
                notes_set = notes_set.filter(favorite=False)

    for each_key in type_keys_out:
        notes_set = notes_set.exclude(type=each_key)

    return render(request, 'main.html', context={'notes': notes_set})


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


class LoginToProfileView(LoginView):
    template_name = 'login.html'
    next_page = 'profile'
