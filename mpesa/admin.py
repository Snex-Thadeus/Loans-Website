from django.contrib import admin
from mpesa.models import LNMLoan

# Register your models here.

class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")

admin.site.register(LNMLoan, LNMOnlineAdmin)