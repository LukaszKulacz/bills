from django.test import TestCase
from bills.models import Bill, Room, Payment
from math import floor
# Create your tests here.

def gr(value) -> int:
    return value * 100


class BillTestCase(TestCase):
    def setUp(self):
        self.room_big = Room.objects.create(
            name='Większy pokój', first_name='Adam', last_name='Adamowski', 
            mail='adam@gmail.com', phone='123-123-123', date_from='2023-01-01', date_to='2023-10-01'
        )
        self.room_small = Room.objects.create(
            name='Mniejszy pokój', first_name='Jan', last_name='Janowski', 
            mail='jan@gmail.com', phone='234-234-234', date_from='2022-01-01', date_to='2022-10-01'
        )

    def test_rent_for_each_room(self):
        Bill.objects.create(type=Bill.BillType.RENT, room=self.room_big, value_to_pay=gr(1250.00))
        Bill.objects.create(type=Bill.BillType.RENT, room=self.room_small, value_to_pay=gr(950.00))
        self.assertEqual(Bill.objects.count(), 2)
        self.assertEqual(Payment.objects.count(), 2)
        self.assertEqual(Payment.objects.get(room=self.room_big.id).bill.value_to_pay, gr(1250.00))
        self.assertEqual(Payment.objects.get(room=self.room_small.id).bill.value_to_pay, gr(950.00))

    def test_rent_payment(self):
        bill = Bill.objects.create(type=Bill.BillType.RENT, room=self.room_big, value_to_pay=gr(1250.00))
        self.assertEqual(Bill.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(len(Payment.objects.filter(room=self.room_big)), 1)
        self.assertEqual(len(Payment.objects.filter(room=self.room_small)), 0)

        pay = Payment.objects.get(room=self.room_big)
        pay.value = gr(1000.0)
        pay.save()

        self.assertEqual(Payment.objects.get(room=self.room_big).balance(), gr(-250.0))
        self.assertEqual(Bill.objects.get(id=bill.id).balance(), gr(-250.0))
        self.assertFalse(Payment.objects.get(room=self.room_big).is_paid())
        self.assertFalse(Bill.objects.get(id=bill.id).is_paid())

        pay.value = gr(1250.0)
        pay.save()

        self.assertEqual(Payment.objects.get(room=self.room_big).balance(), 0)
        self.assertEqual(Bill.objects.get(id=bill.id).balance(), 0)
        self.assertTrue(Payment.objects.get(room=self.room_big).is_paid())
        self.assertTrue(Bill.objects.get(id=bill.id).is_paid())

    def test_bill_split(self):
        bill = Bill.objects.create(type=Bill.BillType.ELECTRIC, value_to_pay=gr(559.41))
        self.assertEqual(Bill.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 2)
        self.assertFalse(self.room_big.is_paid())
        self.assertFalse(self.room_small.is_paid())
        
        pay_big = Payment.objects.get(room=self.room_big)
        pay_small = Payment.objects.get(room=self.room_small)
        self.assertEqual(pay_big.value_to_pay, pay_small.value_to_pay)

        pay_big.value = pay_big.value_to_pay
        pay_big.save()
        self.assertTrue(self.room_big.is_paid())
        self.assertFalse(self.room_small.is_paid())
        self.assertFalse(bill.is_paid())

    def test_more_rooms(self):
        room_add = Room.objects.create(
            name='Dodatkowy pokój', first_name='Ania', last_name='Aniowska', 
            mail='ania@gmail.com', phone='345-345-345', date_from='2022-06-01', date_to='2023-09-01'
        )
        Bill.objects.create(type=Bill.BillType.RENT, value_to_pay=gr(1250.53))
        self.assertEqual(Bill.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 3)
        for pay in Payment.objects.all():
            self.assertEqual(pay.value_to_pay,  int(floor(gr(1250.53) / 3 )))

    def test_remove_rent(self):
        bill_org = Bill.objects.create(type=Bill.BillType.RENT, value_to_pay=gr(1250.00))
        bill_get = Bill.objects.get(id=bill_org.id)
        bill_get.delete()
        self.assertEqual(Bill.objects.count(), 0)
        self.assertEqual(Payment.objects.count(), 0)
        


