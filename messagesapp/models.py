from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiated_convo")
    other = models.ForeignKey(User, on_delete=models.CASCADE, related_name="other_party")
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        initiator_name = self.initiator.username
        other_name = self.other.username
        return f'({initiator_name}, {other_name})'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_message")
    convo = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="conversation_messages")
    content = models.CharField(max_length=1000) 
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        sender_name = self.sender.username
        receiver_name = self.receiver.username
        return f'({self.content}, {sender_name}, {receiver_name})'
