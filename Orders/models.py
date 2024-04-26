import uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Orders(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.JSONField(default=list)  
    
    def __str__(self):
        return str(self.order_id)

@receiver(post_save, sender=Orders)
def update_payment_status(sender, instance, created, **kwargs):
    # If the order is newly created and payment status is pending
    if created and instance.payment_status == Orders.PENDING:
        # Assume here payment confirmation logic
        # Check if payment is successful, update to completed status
        if instance.payment_status == Orders.COMPLETED:
            instance.payment_status = Orders.COMPLETED
            instance.save()
        # Check if payment failed, update to cancelled status
        elif instance.payment_status == Orders.CANCELLED:
            instance.payment_status = Orders.CANCELLED
            instance.save()

