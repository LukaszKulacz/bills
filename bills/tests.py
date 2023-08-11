from django.test import TestCase
from bills.models import Bill, Room, Payment
# Create your tests here.


class BillTestCase(TestCase):
    def setUp(self):
        self.room_big = Room.objects.create(name='BIG', first_name='b', last_name='B', area=20.0)
        self.room_small = Room.objects.create(name='SMALL', first_name='s', last_name='S', area=10.0)

    def test_all_rooms_rent(self):
        Bill.objects.create(bill_type=Bill.BillType.RENT, amount=1250)
        self.assertEqual(Bill.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 2)

    def test_single_room_rent(self):
        Bill.objects.create(bill_type=Bill.BillType.RENT, room=self.room_big, amount=1250)
        self.assertEqual(Bill.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(len(Payment.objects.filter(room=self.room_big)), 1)
        self.assertEqual(len(Payment.objects.filter(room=self.room_small)), 0)

    def test_more_rooms(self):
        room_add = Room.objects.create(name='ADD', first_name='c', last_name='C', area=20.0)
        Bill.objects.create(bill_type=Bill.BillType.RENT, amount=1250)
        self.assertEqual(Bill.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 3)
        for pay in Payment.objects.all():
            self.assertEqual(pay.amount_to_pay, 1250 / 3)

    def test_remove_rent(self):
        bill_org = Bill.objects.create(bill_type=Bill.BillType.RENT, amount=1250)
        bill_get = Bill.objects.get(id=bill_org.id)
        bill_get.delete()
        self.assertEqual(Bill.objects.count(), 0)
        self.assertEqual(Payment.objects.count(), 0)
