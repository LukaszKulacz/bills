from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("room/<int:room_id>", views.room, name="room"),
    path("payment/<int:payment_id>", views.payment, name="payment"),
    path("bill/add/<str:bill_type>", views.bill, name="add_bill"),
    path("bill/edit/<str:bill_type>/<int:bill_id>", views.bill, name="edit_bill"),
    path("bill/delete/<int:bill_id>", views.delete_bill, name="delete_bill"),
    path("rent/<int:room_id>/add", views.bill, name="add_rent"),
    path("rent/<int:room_id>/edit/<int:bill_id>", views.bill, name="edit_rent"),
]
