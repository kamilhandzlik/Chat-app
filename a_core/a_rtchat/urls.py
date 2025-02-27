from django.urls import path
from zope.interface import named

from . import views

urlpatterns = [
    path('',  views.chat_view, name='home'),
    path('chat/<username>', views.get_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom>', views.chat_view, name='chatroom'),
    path('chat/new_groupchat/', views.create_groupchat, name='new-groupchat'),
    path('chat/edit/<chatroom_name>', views.chatroom_edit_view, name='edit-chatroom'),
    path('chat/fileupload/<chatroom_name>', views.chat_file_upload, name='chat-file-upload'),
]