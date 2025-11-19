from django.urls import path
from .views import PrediccionSenasView
from chatMessages.views import ChatListCreateView, ChatDetailView, MessageCreateView

urlpatterns = [
    path('load-image/', PrediccionSenasView.as_view()),
    path('chats/', ChatListCreateView.as_view(), name='chat-list'),
    path('chats/<uuid:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('messages/', MessageCreateView.as_view(), name='message-create'),
]

