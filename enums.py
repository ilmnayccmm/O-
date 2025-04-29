from enum import Enum


class TransactionType(Enum):
    RECEIPT = "Надходження"
    SHIPMENT = "Відвантаження"
    TRANSFER = "Переміщення"