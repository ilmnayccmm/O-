from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TransactionType(Enum):
    RECEIPT = "Надходження"
    SHIPMENT = "Відвантаження"
    TRANSFER = "Переміщення"


class Supplier:

    def __init__(self, name: str, email: str, phone: str, address: str):
        self._validate_supplier_data(name, email, phone)
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def _validate_supplier_data(self, name: str, email: str, phone: str) -> None:
        if not name or len(name) < 2:
            raise ValueError("Назва компанії повинна містити щонайменше 2 символи")

        if not self._validate_email(email):
            raise ValueError("Невірний формат електронної адреси")

        if not self._validate_phone(phone):
            raise ValueError("Невірний формат номера телефону")

    @staticmethod
    def _validate_email(email: str) -> bool:
        if not email or '@' not in email:
            return False

        local_part, domain_part = email.rsplit('@', 1)

        if not local_part or ' ' in local_part:
            return False

        if not domain_part or '.' not in domain_part:
            return False

        domain, extension = domain_part.rsplit('.', 1)

        if not domain or not extension or len(extension) < 2:
            return False

        return True

    @staticmethod
    def _validate_phone(phone: str) -> bool:
        if not phone:
            return False

        if phone.startswith('+'):
            phone = phone[1:]

        if not phone.isdigit():
            return False

        if len(phone) < 10 or len(phone) > 15:
            return False

        return True

    def __str__(self) -> str:
        return f"{self.name} (тел: {self.phone}, email: {self.email})"


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


def display_menu():
    print("\n" + "=" * 50)
    print("СИСТЕМА УПРАВЛІННЯ СКЛАДОМ".center(50))
    print("=" * 50)
    print("1. Додати нового постачальника")
    print("2. Додати новий товар")
    print("3. Переглянути всі товари")
    print("4. Переглянути товари (сортування)")
    print("5. Переглянути всіх постачальників")
    print("6. Переглянути товари постачальника")
    print("7. Видалити товар (відвантажити)")
    print("8. Оновити інформацію про товар")
    print("9. Переглянути історію операцій")
    print("0. Вихід")
    print("=" * 50)


def get_int_input(prompt: str, min_value: int = None, max_value: int = None) -> int:
    while True:
        try:
            value = int(input(prompt))

            if min_value is not None and value < min_value:
                print(f"Значення повинно бути не менше {min_value}")
                continue

            if max_value is not None and value > max_value:
                print(f"Значення повинно бути не більше {max_value}")
                continue

            return value
        except ValueError:
            print("Будь ласка, введіть ціле число")


def get_float_input(prompt: str, min_value: float = None) -> float:
    while True:
        try:
            value = float(input(prompt))

            if min_value is not None and value < min_value:
                print(f"Значення повинно бути не менше {min_value}")
                continue

            return value
        except ValueError:
            print("Будь ласка, введіть число")


def add_supplier(warehouse: Warehouse) -> None:
    print("\n--- Додавання нового постачальника ---")

    name = input("Введіть назву компанії: ")
    email = input("Введіть email: ")
    phone = input("Введіть телефон: ")
    address = input("Введіть адресу: ")

    try:
        supplier = Supplier(name, email, phone, address)
        warehouse.add_supplier(supplier)
        print(f"Постачальник '{name}' успішно доданий")
    except ValueError as e:
        print(f"Помилка: {e}")


def add_product(warehouse: Warehouse) -> None:
    print("\n--- Додавання нового товару ---")

    if not warehouse.suppliers:
        print("Спочатку додайте хоча б одного постачальника")
        return

    name = input("Введіть назву товару: ")
    quantity = get_int_input("Введіть кількість: ", 1)
    price = get_float_input("Введіть ціну за одиницю: ", 0.01)
    description = input("Введіть опис (необов'язково): ")

    print("\nДоступні постачальники:")
    suppliers = warehouse.get_all_suppliers()
    for i, supplier in enumerate(suppliers, 1):
        print(f"{i}. {supplier.name}")

    supplier_idx = get_int_input("Оберіть постачальника (номер): ", 1, len(suppliers)) - 1
    selected_supplier = suppliers[supplier_idx]

    try:
        product = Product(name, quantity, price, selected_supplier, description=description)
        warehouse.add_product(product)
        print(f"Товар '{name}' успішно доданий на склад")
    except (ValueError) as e:
        print(f"Помилка: {e}")


def display_all_products(warehouse: Warehouse) -> None:
    print("\n--- Список всіх товарів на складі ---")

    products = warehouse.get_all_products()

    if not products:
        print("Склад порожній")
        return

    print(f"{'Назва':<30} {'Кількість':<10} {'Ціна, грн':<15} {'Постачальник':<20}")
    print("-" * 75)

    for product in products:
        print(f"{product.name:<30} {product.quantity:<10} {product.price:<15.2f} {product.supplier.name:<20}")


def display_sorted_products(warehouse: Warehouse) -> None:
    print("\n--- Сортування товарів ---")

    if not warehouse.products:
        print("Склад порожній")
        return

    print("Виберіть критерій сортування:")
    print("1. За назвою")
    print("2. За кількістю")
    print("3. За ціною")

    choice = get_int_input("Ваш вибір: ", 1, 3)

    sort_keys = {1: 'name', 2: 'quantity', 3: 'price'}
    sort_key = sort_keys[choice]

    products = warehouse.get_products_sorted(sort_key)

    print(f"\n{'Назва':<30} {'Кількість':<10} {'Ціна, грн':<15} {'Постачальник':<20}")
    print("-" * 75)

    for product in products:
        print(f"{product.name:<30} {product.quantity:<10} {product.price:<15.2f} {product.supplier.name:<20}")


def display_all_suppliers(warehouse: Warehouse) -> None:
    print("\n--- Список всіх постачальників ---")

    suppliers = warehouse.get_all_suppliers()

    if not suppliers:
        print("Немає зареєстрованих постачальників")
        return

    print(f"{'Назва':<30} {'Телефон':<15} {'Email':<25} {'Адреса':<30}")
    print("-" * 100)

    for supplier in suppliers:
        print(f"{supplier.name:<30} {supplier.phone:<15} {supplier.email:<25} {supplier.address:<30}")


def display_supplier_products(warehouse: Warehouse) -> None:
    print("\n--- Товари постачальника ---")

    if not warehouse.suppliers:
        print("Немає зареєстрованих постачальників")
        return

    print("Виберіть постачальника:")
    suppliers = warehouse.get_all_suppliers()
    for i, supplier in enumerate(suppliers, 1):
        print(f"{i}. {supplier.name}")

    supplier_idx = get_int_input("Ваш вибір: ", 1, len(suppliers)) - 1
    selected_supplier = suppliers[supplier_idx]

    try:
        products = warehouse.get_supplier_products(selected_supplier.name)

        if not products:
            print(f"У постачальника '{selected_supplier.name}' немає товарів на складі")
            return

        print(f"\nТовари постачальника '{selected_supplier.name}':")
        print(f"{'Назва':<30} {'Кількість':<10} {'Ціна, грн':<15}")
        print("-" * 55)

        for product in products:
            print(f"{product.name:<30} {product.quantity:<10} {product.price:<15.2f}")

    except ValueError as e:
        print(f"Помилка: {e}")


def remove_product(warehouse: Warehouse) -> None:
    print("\n--- Відвантаження товару ---")

    if not warehouse.products:
        print("Склад порожній")
        return

    print("Виберіть товар для відвантаження:")
    products = warehouse.get_all_products()
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name} (доступно: {product.quantity} шт)")

    product_idx = get_int_input("Ваш вибір: ", 1, len(products)) - 1
    selected_product = products[product_idx]

    quantity = get_int_input(f"Введіть кількість для відвантаження (макс. {selected_product.quantity}): ",
                             1, selected_product.quantity)

    try:
        warehouse.remove_product(selected_product.name, quantity)
        print(f"Успішно відвантажено {quantity} шт. товару '{selected_product.name}'")
    except ValueError as e:
        print(f"Помилка: {e}")


def update_product_info(warehouse: Warehouse) -> None:
    print("\n--- Оновлення інформації про товар ---")

    if not warehouse.products:
        print("Склад порожній")
        return

    print("Виберіть товар для оновлення:")
    products = warehouse.get_all_products()
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name}")

    product_idx = get_int_input("Ваш вибір: ", 1, len(products)) - 1
    selected_product = products[product_idx]

    print(f"\nПоточна інформація:")
    print(f"Назва: {selected_product.name}")
    print(f"Кількість: {selected_product.quantity}")
    print(f"Ціна: {selected_product.price:.2f} грн")
    print(f"Постачальник: {selected_product.supplier.name}")

    print("\nЩо бажаєте оновити?")
    print("1. Кількість")
    print("2. Ціну")
    print("3. Обидва параметри")

    update_choice = get_int_input("Ваш вибір: ", 1, 3)

    new_quantity = None
    new_price = None

    if update_choice in [1, 3]:
        new_quantity = get_int_input("Введіть нову кількість: ", 0)

    if update_choice in [2, 3]:
        new_price = get_float_input("Введіть нову ціну: ", 0.01)

    try:
        warehouse.update_product_info(selected_product.name, new_quantity, new_price)
        print(f"Інформація про товар '{selected_product.name}' успішно оновлена")
    except ValueError as e:
        print(f"Помилка: {e}")


def display_transactions(warehouse: Warehouse) -> None:
    print("\n--- Історія операцій на складі ---")

    transactions = warehouse.transactions

    if not transactions:
        print("Історія операцій порожня")
        return

    print(f"{'Тип операції':<15} {'Товар':<30} {'Кількість':<10} {'Дата і час':<20}")
    print("-" * 75)

    for transaction in transactions:
        print(f"{transaction.transaction_type.value:<15} {transaction.product.name:<30} "
              f"{transaction.quantity:<10} {transaction.date.strftime('%d.%m.%Y %H:%M'):<20}")


def main():
    warehouse = Warehouse("Головний склад")

    try:
        supplier1 = Supplier("ТОВ Технології", "tech@example.com", "+380991234567", "м. Київ, вул. Центральна 1")
        supplier2 = Supplier("ПП Електроніка", "electro@example.com", "+380972345678", "м. Львів, вул. Головна 45")

        warehouse.add_supplier(supplier1)
        warehouse.add_supplier(supplier2)

        product1 = Product("Ноутбук Dell XPS", 10, 45000.0, supplier1)
        product2 = Product("Смартфон Samsung Galaxy", 20, 15000.0, supplier1)
        product3 = Product("Планшет Apple iPad", 15, 30000.0, supplier2)

        warehouse.add_product(product1)
        warehouse.add_product(product2)
        warehouse.add_product(product3)

        print("Тестові дані успішно додані.")
    except Exception as e:
        print(f"Помилка при додаванні тестових даних: {e}")

    while True:
        display_menu()
        choice = get_int_input("Виберіть опцію: ", 0, 9)

        if choice == 0:
            print("\nДякуємо за використання системи управління складом!")
            break
        elif choice == 1:
            add_supplier(warehouse)
        elif choice == 2:
            add_product(warehouse)
        elif choice == 3:
            display_all_products(warehouse)
        elif choice == 4:
            display_sorted_products(warehouse)
        elif choice == 5:
            display_all_suppliers(warehouse)
        elif choice == 6:
            display_supplier_products(warehouse)
        elif choice == 7:
            remove_product(warehouse)
        elif choice == 8:
            update_product_info(warehouse)
        elif choice == 9:
            display_transactions(warehouse)


if __name__ == "__main__":
    main()