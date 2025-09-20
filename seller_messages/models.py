from django.db import models


class SellerMessagesSellermessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField()
    created_at = models.DateTimeField()
    receiver = models.ForeignKey('UsersUser', models.DO_NOTHING)
    sender = models.ForeignKey('UsersUser', models.DO_NOTHING, related_name='sellermessagessellermessage_sender_set')

    class Meta:
        managed = False
        db_table = 'seller_messages_sellermessage'
        