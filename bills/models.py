from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    area = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name}: {self.first_name} {self.last_name}'

    def calc_balance(self):
        pays = Payment.objects.filter(room=self.id)
        total = sum([pay.amount_to_pay for pay in pays])
        sent = sum([pay.amount for pay in pays])
        return sent - total


class Bill(models.Model):
    class BillType(models.TextChoices):
        RENT = "RENT", _("Czynsz")
        HOUSING = "HOUSING", _("Spółdzielnia")
        ELECTRIC = "ELECTRIC", _("Prąd")
        GAS = "GAS", _("Gaz")
        OTHER = "OTHER", _("Inne")

    bill_type = models.CharField(max_length=50, choices=BillType.choices, default=BillType.HOUSING)
    date = models.DateField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=200, default='', blank=True)
    payments_created = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bill_type} : {self.date}'

    def calc_balance(self):
        payments = Payment.objects.filter(bill=self.id)
        paid = sum([pay.amount for pay in payments])
        return paid - self.amount

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Bill, self).save(force_insert, force_update, using, update_fields)
        if self.payments_created:
            for pay in Payment.objects.filter(bill=self):
                pay.amount_to_pay = self.amount / len(Payment.objects.filter(bill=self.id))
                pay.save()
        else:
            if self.room is None:
                rooms = Room.objects.all()
                for room in rooms:
                    Payment(bill=self, room=room, amount_to_pay=self.amount / len(rooms), amount=0).save()
            else:
                Payment(bill=self, room=self.room, amount_to_pay=self.amount, amount=0).save()
            self.payments_created = True
            self.save()


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount_to_pay = models.DecimalField(max_digits=7, decimal_places=2)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return f'{self.bill}: {self.amount}/{self.amount_to_pay}'


