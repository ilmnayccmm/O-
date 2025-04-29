from warehouse import Warehouse
from supplier import Supplier
from product import Product


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