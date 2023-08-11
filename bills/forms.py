from django import forms
from .models import Bill, Room


class BillAdminForm(forms.ModelForm):
    def clean(self):
        pass
        # raise forms.ValidationError({'amount': 'sadasd'})


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ["amount", "description"]

    # bill_type = forms.ChoiceField(choices=Bill.BillType.choices, disabled=False)


class RentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        for room in Room.objects.all():
            self.fields[f'{room.id}'] = forms.DecimalField(max_digits=6, decimal_places=2)
