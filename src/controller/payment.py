from src.model.payment_repository import PaymentRepository
from src import models

class PaymentUseCase:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    def process_payment(self, order_id: int, method: models.PaymentMethod):
        self.payment_repo.confirm_payment(order_id)
        if method == models.PaymentMethod.pix:
            return { "message": "Pagamento via Pix confirmado" }
        elif method == models.PaymentMethod.credit_card:
            return { "message": "Pagamento via cartão de crédito aprovado" }
        elif method == models.PaymentMethod.debit_card:
            return { "message": "Pagamento via cartão de débito aprovado" }
        else:
            raise ValueError("Método de pagamento inválido")
