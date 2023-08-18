from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as user_logout, login as user_login
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.template.defaultfilters import date
from .models import Room, Payment, Bill
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            return redirect('index')
        else:
            return render(request, 'login_form.html', {"failed": True})    
    else:
        return render(request, 'login_form.html')


@login_required(login_url="login")
def logout(request):
    user_logout(request)
    return redirect('login')


@login_required(login_url="login")
def index(request):
    rooms = Room.objects.all()
    data = {
        "rooms": rooms,
        "rooms_balance": sum([room.balance() for room in rooms]),
        "bills": Bill.get_all_grouped_by_month(),
        "types": Bill.BillType.choices[1:]
    }
    return render(request, 'home.html', data)


@login_required(login_url="login")
def room(request, room_id: int):
    room = Room.objects.get(id=room_id)
    data = {
        "room": room,
        "payments": Payment.get_grouped_by_month(room=room)
    }

    return render(request, 'room.html', data)


@login_required(login_url="login")
def bill_create(request, type: Bill.BillType):
    if request.method == 'POST':
        try:
            Bill(
                type=type, 
                date_created=parse_date(request.POST['date_created'] + '-01'),
                room=None,
                value_to_pay=int(float(request.POST['value_to_pay']) * 100),
                description=request.POST['description']
            ).save()
        except Exception as err:
            print('bill_create: ', err)

        return redirect('index')  # ADD toast etc.
    else: 
        last_bill = Bill.objects.filter(type=type).order_by('-date_created').first()

        data = {
            "type": Bill.BillType(type).label,
            "now": timezone.now().strftime('%Y-%m'),
            "value": "",
            "description": "",
        }
                
        if last_bill is not None:
            data['last_bill'] = {
                "value_to_pay": str(last_bill.format_value_to_pay()),
                "date_created": last_bill.date_created.strftime('%Y-%m')
            }

        return render(request, 'bill_form.html', data)
        

@login_required(login_url="login")
def bill_update(request, bill_id: int):
    bill = Bill.objects.get(id=bill_id)
    if request.method == 'POST':
        try:
            bill.date_created=parse_date(request.POST['date_created'] + '-01')
            bill.value_to_pay=int(float(request.POST['value_to_pay']) * 100)
            bill.description=request.POST['description']
            bill.save()
        except Exception as err:
            print('bill_update: ', err)

        return redirect('index')  # ADD toast etc.
    else: 
        data = {
            "type": bill.get_type_display(),
            "now": bill.date_created.strftime('%Y-%m'),
            "value": str(bill.format_value_to_pay()).replace(',', '.'),
            "description": bill.description,
            "bill_id": bill_id
        }
        return render(request, 'bill_form.html', data)


@login_required(login_url="login")
def bill_delete(request, bill_id: int):
    bill = Bill.objects.get(id=bill_id)
    bill.delete()
    return redirect('index')


@login_required(login_url="login")
def rent_create(request, room_id: int):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        try:
            Bill(
                type=Bill.BillType.RENT, 
                date_created=parse_date(request.POST['date_created'] + '-01'),
                room=room,
                value_to_pay=int(float(request.POST['value_to_pay']) * 100),
                description=request.POST['description']
            ).save()
        except Exception as err:
            print('rent_create: ', err)

        return redirect('index')  # ADD toast etc.
    else: 
        last_bill = Bill.objects.filter(room=room, type=Bill.BillType.RENT).order_by('-date_created').first()

        data = {
            "type": Bill.BillType.RENT.label,
            "now": timezone.now().strftime('%Y-%m'),
            "room": room,
            "value": "",
            "description": "",
            "bill_id": None
        }
        if last_bill is not None:
            data['last_bill'] = {
                "value_to_pay": str(last_bill.format_value_to_pay()),
                "date_created": last_bill.date_created.strftime('%Y-%m')
            }

        return render(request, 'bill_form.html', data)


@login_required(login_url="login")
def rent_update(request, bill_id: int):
    bill = Bill.objects.get(id=bill_id)
    if request.method == 'POST':
        try:
            bill.date_created=parse_date(request.POST['date_created'] + '-01')
            bill.value_to_pay=int(float(request.POST['value_to_pay']) * 100)
            bill.description=request.POST['description']
            bill.save()
        except Exception as err:
            print('rent_update: ', err)

        return redirect('index')  # ADD toast etc.
    else: 
        data = {
            "type": Bill.BillType.RENT.label,
            "now": bill.date_created.strftime('%Y-%m'),
            "room": bill.room,
            "value": str(bill.format_value_to_pay()).replace(',', '.'),
            "description": bill.description,
            "bill_id": bill_id
        }
        #if bill.room is not None:
        #    data['room'] = bill.room
        return render(request, 'bill_form.html', data)


@login_required(login_url="login")
def rent_delete(request, bill_id: int):
    return bill_delete(request, bill_id)


@login_required(login_url="login")
def payment_update(request, payment_id: int):
    pay = Payment.objects.get(id=payment_id)
    if request.method == 'POST':
        if 'action_update' in request.POST:
            pay.value = int(float(request.POST['value_to_pay']) * 100)
        elif 'action_full_payment' in request.POST:
            pay.value = pay.value_to_pay
        elif 'action_clear_payment' in request.POST:
            pay.value = 0

        pay.save()
        return redirect('room', room_id=pay.room_id)
    else:
        data = {
            "payment": pay,
            "date_created": pay.date_created.strftime('%Y-%m'),
            "value": str(pay.format_value()).replace(',','.'),
            "value_to_pay": str(pay.format_value_to_pay()).replace(',','.')
        }
        return render(request, 'payment_form.html', data)


@login_required(login_url="login")
def summary(request):
    text = 'Os. Piastowskie 23/10 \n'
    text += f'Data wygenerowania podsumowania {date(timezone.now(), "d F Y")}: \n\n'
    for room in Room.objects.all():
        text += f'{room.name} - {room.first_name} {room.last_name} \n'

        if room.balance() > 0:
            text += f'Nadpłata: {room.balance()} zł \n'
        elif room.balance() < 0:
            text += f'Niedopłata: {-room.balance()} zł \n'
        else:
            text += 'Saldo: 0.00 zł \n'

        payments = Payment.objects.filter(room=room, paid=False)
        if len(payments) > 0:
            text += f'Rachunki: \n'
            for payment in payments:
                text += f'- {payment.bill.get_type_display()} {payment.description} {date(payment.date_created, "F")} zapłacono {payment.value/100:.2f} z {payment.value_to_pay/100:.2f} ('
                if payment.balance() > 0:
                    text += f'nadpłata {payment.balance():.2f})\n'
                else:
                    text += f'niedopłata {-payment.balance():.2f})\n'
        text += '\n'

    data = {
        "mail": "alina@goldenloft.nieruchomosci.pl",
        "mail_subject": f'Os. Piastowskie 23/10 - {date(timezone.now(), "F Y")}',
        "mail_body": text.replace('\n', '%0D%0A'),
        "summary": text.replace('\n', '<br />'),
        "raw_summary": text
    }
    return render(request, 'summary.html', data)