from datetime import datetime
from supplier import Supplier


class Product:

    def __init__(
            self,
            name: str,
            quantity: int,
            price: float,
            supplier: Supplier,
            arrival_date: datetime = None,
            description: str = "",
    ):
        self._validate_product_data(name, quantity, price)
        self.name = name
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        self.arrival_date = arrival_date or datetime.now()
        self.description = description

    @staticmethod
    def _validate_product_data(name: str, quantity: int, price: float) -> None:
        if not name or len(name) < 3:
            raise ValueError("Назва товару повинна містити щонайменше 3 символи")

        if quantity < 0:
            raise ValueError("Кількість товару не може бути від'ємною")

        if price <= 0:
            raise ValueError("Ціна товару повинна бути більше нуля")

    def update_quantity(self, new_quantity: int) -> None:
        if new_quantity < 0:
            raise ValueError("Кількість товару не може бути від'ємною")
        self.quantity = new_quantity

    def update_price(self, new_price: float) -> None:
        if new_price <= 0:
            raise ValueError("Ціна товару повинна бути більше нуля")
        self.price = new_price

    def __str__(self) -> str:
        return f"{self.name} - {self.quantity} шт., {self.price} грн/шт."