from django.db import models
import uuid

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title or f"Chat {self.id}"
    
class Message(models.Model):
    SENDER_CHOICES = (
        ('USER', 'Usuario'),
        ('AI', 'Inteligencia Artificial'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    
    text = models.TextField() 
    
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.chat.title or 'Chat'} | {self.sender}]: {self.text[:50]}..."