from typing import List, Dict, Optional
from supplier import Supplier
from product import Product
from transaction import Transaction
from enums import TransactionType


class Warehouse:

    def __init__(self, name: str):
        self.name = name
        self.products: Dict[str, Product] = {}
        self.suppliers: Dict[str, Supplier] = {}
        self.transactions: List[Transaction] = []

    def add_supplier(self, supplier: Supplier) -> None:
        if supplier.name in self.suppliers:
            raise ValueError(f"Постачальник з назвою '{supplier.name}' вже існує")
        self.suppliers[supplier.name] = supplier

    def add_product(self, product: Product) -> None:
        if product.supplier.name not in self.suppliers:
            raise ValueError(f"Постачальник '{product.supplier.name}' не зареєстрований")

        if product.name in self.products:
            existing_product = self.products[product.name]
            existing_product.quantity += product.quantity
            existing_product.update_price(product.price)
        else:
            self.products[product.name] = product

        self.transactions.append(
            Transaction(product, product.quantity, TransactionType.RECEIPT)
        )

    def remove_product(self, product_name: str, quantity: int) -> None:
        if product_name not in self.products:
            raise ValueError(f"Товар '{product_name}' не знайдено на складі")

        product = self.products[product_name]

        if quantity > product.quantity:
            raise ValueError(f"Недостатня кількість товару на складі. Доступно: {product.quantity}")

        product.update_quantity(product.quantity - quantity)

        self.transactions.append(
            Transaction(product, quantity, TransactionType.SHIPMENT)
        )

        if product.quantity == 0:
            del self.products[product_name]

    def update_product_info(
        self,
        product_name: str,
        new_quantity: Optional[int] = None,
        new_price: Optional[float] = None,
    ) -> None:
        if product_name not in self.products:
            raise ValueError(f"Товар '{product_name}' не знайдено на складі")

        product = self.products[product_name]

        if new_quantity is not None:
            product.update_quantity(new_quantity)

        if new_price is not None:
            product.update_price(new_price)

    def get_all_products(self) -> List[Product]:
        return list(self.products.values())

    def get_products_sorted(self, sort_key: str) -> List[Product]:
        if sort_key not in ['name', 'quantity', 'price']:
            raise ValueError("Неправильний ключ сортування. Доступні: 'name', 'quantity', 'price'")

        return sorted(self.products.values(), key=lambda p: getattr(p, sort_key))

    def get_supplier_products(self, supplier_name: str) -> List[Product]:
        if supplier_name not in self.suppliers:
            raise ValueError(f"Постачальник '{supplier_name}' не знайдено")

        return [p for p in self.products.values() if p.supplier.name == supplier_name]

    def get_all_suppliers(self) -> List[Supplier]:
        return list(self.suppliers.values())