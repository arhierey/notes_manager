from django.urls import path

from .views import *

urlpatterns = [
    path('', first_page, name='home'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginToProfileView.as_view(), name='login'),

    path('main/', main_page, name='profile'),

    path('main/new_note/', new_note_page, name='new_note'),
    path('main/new_note/add_note', add_note, name='add_note'),

    path('main/edit_note', edit_note, name='edit_note'),
    path('main/save_edited_note', save_edited_note, name='save_edited_note'),

    path('main/filter_it', filter_it, name='filter_it'),

    path('delete_note', delete_note, name='delete_note'),

    path('main/to_note', go_to_note, name='to_note'),
    path('<int:note_id>/', note_view, name='note_view'),
    path('<int:note_id>/back', back_to_main, name='back'),

    path('main/logout', logout_view, name='logout')
]
