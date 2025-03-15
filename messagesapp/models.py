from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiators")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receivers")
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        initiator_name = self.initiator.username
        receiver_name = self.receiver.username
        return f'({initiator_name} -> {receiver_name} at {self.created.strftime("%Y-%m-%d %H:%M:%S")})'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senders")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipients")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.CharField(max_length=1000) 
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        sender_name = self.sender.username
        recipient_name = self.recipient.username
        content_preview = self.content[:20]
        return f'({sender_name} -> {recipient_name} | {content_preview}...)'
