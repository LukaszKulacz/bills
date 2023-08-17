from django.contrib import admin
from .models import Bill, Room, Payment


class BillAdmin(admin.ModelAdmin):
    list_display = ['type', 'room', 'date_created', 'value_to_pay', 'description']
    
    # def formatted_value_to_pay(self, model):
    #     return f'{model.value_to_pay / 100:.2f} zł'

class RoomAdmin(admin.ModelAdmin):
    pass
    #list_display = ['name', 'first_name', 'last_name', 'area']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bill', 'room', 'value_to_pay', 'value']


admin.site.register(Bill, BillAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Payment, PaymentAdmin)
