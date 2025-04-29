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