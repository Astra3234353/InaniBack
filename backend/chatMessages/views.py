from rest_framework import generics
from .models import Chat, Message
# Nota: Ya no necesitamos ChatListSerializer si siempre quieres ver todo
from .serializers import ChatDetailSerializer, MessageSerializer 


class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all().order_by('-created_at')
    serializer_class = ChatDetailSerializer 

class ChatDetailView(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer
    lookup_field = 'id'


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # 1. Guardar mensaje del usuario
        user_message = serializer.save(sender='USER')
        chat_id = user_message.chat.id
        
        # 2. Respuesta simulada de la IA
        respuesta_texto = f"Recibido: {user_message.text}"

        # 3. Guardar respuesta de IA
        Message.objects.create(
            chat_id=chat_id,
            text=respuesta_texto,
            sender='AI'
        )