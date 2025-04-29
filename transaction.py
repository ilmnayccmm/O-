from datetime import datetime
from product import Product
from enums import TransactionType


class Transaction:

    def __init__(self, product: Product, quantity: int,
                 transaction_type: TransactionType, date: datetime = None):
        self.product = product
        self.quantity = quantity
        self.transaction_type = transaction_type
        self.date = date or datetime.now()

    def __str__(self) -> str:
        return (f"{self.transaction_type.value}: {self.product.name} - "
                f"{self.quantity} шт. ({self.date.strftime('%d.%m.%Y %H:%M')})")