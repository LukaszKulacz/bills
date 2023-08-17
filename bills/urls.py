from django.urls import path

from . import views

urlpatterns = [

    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),

    path("", views.index, name="index"),
    path("room/<int:room_id>", views.room, name="room"),
    path("summary", views.summary, name='summary'),

    path("bill/create/<str:type>", views.bill_create, name="bill_create"),
    path("bill/update/<int:bill_id>", views.bill_update, name="bill_update"),
    path("bill/delete/<int:bill_id>", views.bill_delete, name="bill_delete"),

    path("rent/create/<int:room_id>", views.rent_create, name="rent_create"),
    path("rent/update/<int:bill_id>", views.rent_update, name="rent_update"),
    path("rent/delete/<int:bill_id>", views.rent_delete, name="rent_delete"),

    path("payment/update/<int:payment_id>", views.payment_update, name="payment_update"),



    # path("payment/<int:payment_id>/<int:value>", views.payment, name="full_payment"),
    # path("payment/<int:payment_id>", views.payment, name="payment"),
    
    # path("bill/edit/<str:bill_type>/<int:bill_id>", views.bill, name="edit_bill"),
    # path("bill/delete/<int:bill_id>", views.delete_bill, name="delete_bill"),
    # path("rent/<int:room_id>/add", views.bill, name="add_rent"),
    # path("rent/<int:room_id>/edit/<int:bill_id>", views.bill, name="edit_rent"),
]
