from warehouse import Warehouse
from supplier import Supplier
from product import Product
from menu import (
    display_menu, add_supplier, add_product, display_all_products,
    display_sorted_products, display_all_suppliers, display_supplier_products,
    remove_product, update_product_info, display_transactions, get_int_input
)


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