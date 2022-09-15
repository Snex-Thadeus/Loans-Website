from django.db import models

# Create your models here.

class LNMLoan(models.Model):
    MerchantRequestID = models.CharField(max_length=20, blank=True, null=True)
    CheckoutRequestID = models.CharField(max_length=50, blank=True, null=True)
    Amount = models.FloatField( blank=True, null=True)
    MpesaReceiptNumber = models.CharField(max_length=15, blank=True, null=True)
    Balance = models.CharField(max_length=12, blank=True, null=True)
    TransactionDate = models.DateTimeField( blank=True, null=True)
    PhoneNumber = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
         verbose_name = "LNMLoan"
         verbose_name_plural ="LNMLoans"

    def __str__(self):
        return f"{self.PhoneNumber}has sent {self.Amount}"