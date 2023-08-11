from django.contrib import admin
from .models import Bill, Room, Payment
from .forms import BillAdminForm


class BillAdmin(admin.ModelAdmin):
    form = BillAdminForm
    list_display = ['bill_type', 'room', 'date', 'amount', 'description']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'first_name', 'last_name', 'area']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bill', 'room', 'amount_to_pay', 'amount']


admin.site.register(Bill, BillAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Payment, PaymentAdmin)
