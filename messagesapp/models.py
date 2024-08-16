from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=150)
    secret_question = models.CharField(max_length=200)
    secret_answer = models.CharField(max_length=40)

class Conversations(models.Model):
    initiator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="initiated_convo")
    other = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="other_party")
    deleted = models.BooleanField(default=False)

class Messages(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="received_message")
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE, related_name="conversation_messages")
    content = models.CharField(max_length=1000) 
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
