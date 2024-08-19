from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiated_convo")
    other = models.ForeignKey(User, on_delete=models.CASCADE, related_name="other_party")
    deleted = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_message")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="conversation_messages")
    content = models.CharField(max_length=1000) 
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
