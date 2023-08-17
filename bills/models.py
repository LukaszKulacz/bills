from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import date
from django.utils import timezone
import datetime


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mail = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        # return f'{self.name}: {self.first_name} {self.last_name}'
        return self.name

    def balance(self):
        pays = Payment.objects.filter(room=self.id)
        total = sum([pay.value_to_pay for pay in pays])
        sent = sum([pay.value for pay in pays])
        return (sent - total) / 100
    
    def paid(self):
        return self.balance() == 0


class Bill(models.Model):
    class BillType(models.TextChoices):
        RENT = "RENT", _("Czynsz")
        HOUSING = "HOUSING", _("Spółdzielnia")
        ELECTRIC = "ELECTRIC", _("Prąd")
        GAS = "GAS", _("Gaz")
        OTHER = "OTHER", _("Inne")

    type = models.CharField(max_length=50, choices=BillType.choices, default=BillType.HOUSING)
    date_created = models.DateField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    value_to_pay = models.IntegerField()
    description = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return f'{self.type} : {self.date_created}'
    
    def balance(self):
        payments = Payment.objects.filter(bill=self.id)
        paid = sum([pay.value for pay in payments])
        return (paid - self.value_to_pay) / 100
    
    def format_value_to_pay(self):
        return self.value_to_pay / 100
    
    def paid(self):
        return self.balance() == 0.0
    
    def update_payments(self):
        payments = Payment.objects.filter(bill=self)
        for payment in payments:
            payment.value_to_pay = self.value_to_pay / len(payments)
            payment.date_created = self.date_created
            payment.save()

    def create_payments(self, room=None):
        if room is not None: 
            # create payment for SINGLE room
            Payment(bill=self, room=room, value_to_pay=self.value_to_pay, value=0, date_created=self.date_created).save()
        else:
            # split payments between all rooms
            rooms = Room.objects.all()
            for room in rooms:
                Payment(bill=self, room=room, value_to_pay=self.value_to_pay / len(rooms), value=0, date_created=self.date_created).save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.value_to_pay -= self.value_to_pay % Room.objects.count()
        self.date_created = datetime.date(self.date_created.year, self.date_created.month, 1)
        creating = self.id is None
        super(Bill, self).save(force_insert, force_update, using, update_fields)
        if creating:
            self.create_payments(self.room)
        else:
            self.update_payments() 

    @staticmethod
    def get_all_grouped_by_month():
        all_months = Bill.objects.all().values('date_created').distinct().order_by('-date_created')
        output = []
        
        for month in all_months:
            date_created = month["date_created"]
            name = f'{date(date_created, "F")} {date_created.year}'
            bills = list(Bill.objects.filter(date_created=date_created).order_by('-type'))

            output.append({
                "name": name,
                "bills": bills
            }) 

        return output
        

class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
    value_to_pay = models.IntegerField()
    value = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default='', blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bill}: {self.value}/{self.value_to_pay}'
    
    def balance(self):
        return (self.value - self.value_to_pay) / 100
    
    def format_value(self):
        return self.value / 100
    
    def format_value_to_pay(self):
        return self.value_to_pay / 100
    
    def is_paid(self):
        return self.balance() == 0
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.date_created = datetime.date(self.date_created.year, self.date_created.month, 1)
        self.paid = self.value == self.value_to_pay
        super(Payment, self).save(force_insert, force_update, using, update_fields)
    
    @staticmethod
    def get_grouped_by_month(room):
        all_months = Payment.objects.filter(room=room).values('date_created').distinct().order_by('-date_created')
        output = []
        
        for month in all_months:
            date_created = month["date_created"]
            name = f'{date(date_created, "F")} {date_created.year}'
            payments = list(Payment.objects.filter(room=room, date_created=date_created).order_by('-bill__type'))


            output.append({
                "name": name,
                "payments": payments,
                "balance": sum([payment.balance() for payment in payments])
            }) 

        return output
