# by gaoxin

from django.urls import path
from .views import ShoppingCarView
from .settlement_view import SettlementView
from .payment_view import PaymentView

urlpatterns = [
    path('shopping_car', ShoppingCarView.as_view()),
    path('settlement', SettlementView.as_view()),
    path('payment', PaymentView.as_view()),


]