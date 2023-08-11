from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BillForm, RentForm
from .models import Room, Payment, Bill


# Create your views here.
def index(request):
    rooms_list = Room.objects.all()
    for room in rooms_list:
        room.balance = room.calc_balance()
    bills = Bill.objects.all()
    for bill_obj in bills:
        bill_obj.balance = bill_obj.calc_balance()
    return render(request, 'main.html', {
        "rooms": rooms_list,
        "bills": bills,
        "bill_form": BillForm,
    })


def room(request, room_id: int):
    room_obj = Room.objects.get(id=room_id)
    payments = Payment.objects.filter(room=room_id)
    for pay in payments:
        pay.balance = pay.amount - pay.amount_to_pay
    return render(request, 'room.html', {
        "room": room_obj,
        "payments": payments,
        "balance": room_obj.calc_balance()
    })


def payment(request, payment_id: int):
    pay = Payment.objects.get(id=payment_id)
    pay.amount = pay.amount_to_pay
    pay.save()
    return redirect('room', room_id=pay.room.id)


def bill(request, bill_type: str = None, bill_id: int = None, room_id: int = None):
    print(bill_type, bill_id, room_id)
    if room_id is not None:
        bill_type = Bill.BillType.RENT
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return redirect('index')
    else:
        room = None

    try:
        bill_type = Bill.BillType(bill_type)
    except ValueError:
        return redirect('index')

    if bill_id is None:
        # create
        if request.method == 'POST':
            form = BillForm(request.POST)
            if form.is_valid():
                bill_obj = form.save(commit=False)
                bill_obj.bill_type = bill_type
                if room is not None:
                    bill_obj.room = room
                bill_obj.save()
                return redirect('index')

        try:
            last_bill = Bill.objects.filter(bill_type=bill_type, room=room_id).last()
        except Bill.DoesNotExist:
            last_bill = None

        action = reverse('add_bill', args=[bill_type]) if room is None else reverse('add_rent', args=[room_id])

        return render(request, 'bill.html', {
            'action': action,
            'form': BillForm(initial={'amount': last_bill.amount if last_bill is not None else 0.0}),
            'bill_type': bill_type,
            'last_bill': {
                'date': last_bill.date,
                'amount': last_bill.amount
            } if last_bill else None,
            'bill_to_edit': None,
            'room': room
        })
    else:
        # edit
        try:
            bill_obj = Bill.objects.get(id=bill_id)

            if request.method == 'POST':
                form = BillForm(instance=bill_obj, data=request.POST)
                if form.is_valid():
                    form.save(commit=True)
                    return redirect('index')

            action = reverse('edit_bill', args=[bill_type, bill_id]) if room is None else \
                reverse('edit_rent', args=[room_id, bill_id])

            return render(request, 'bill.html', {
                'action': action,
                'form': BillForm(initial={'amount': bill_obj.amount, 'description': bill_obj.description}),
                'bill_type': bill_type,
                'last_bill': None,
                'bill_to_edit': bill_obj,
                'room': room
            })
        except Bill.DoesNotExist:
            return redirect('index')


def delete_bill(request, bill_id: int):
    try:
        bill = Bill.objects.get(id=bill_id)
        bill.delete()
    except Bill.DoesNotExist:
        pass
    return redirect('index')
