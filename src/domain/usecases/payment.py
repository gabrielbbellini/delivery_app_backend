from src.model.payment_repository import PaymentRepository
from src.domain.entities.order import PaymentMethod

class PaymentUseCase:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    def process_payment(self, order_id: int, method: PaymentMethod):
        self.payment_repo.confirm_payment(order_id)
        if method == PaymentMethod.pix:
            return { "message": "Pagamento via Pix confirmado" }
        elif method == PaymentMethod.credit_card:
            return { "message": "Pagamento via cartão de crédito aprovado" }
        elif method == PaymentMethod.debit_card:
            return { "message": "Pagamento via cartão de débito aprovado" }
        else:
            raise ValueError("Método de pagamento inválido")
