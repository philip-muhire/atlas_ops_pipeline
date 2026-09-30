from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repository import Repository
from src.db_models import CustomerModel, TicketModel, OrderModel
from src.schemas import CustomerCreate, TicketCreate, OrderCreate

class OperationsService:
    def __init__(self, db: Session):
        self.repo = Repository(db)

    # --- CUSTOMERS ---
    def list_customers(self, skip: int, limit: int):
        return self.repo.get_all(CustomerModel, skip, limit)

    def create_customer(self, dto: CustomerCreate):
        existing = self.repo.get_by_id(CustomerModel, "customer_id", dto.customer_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer '{dto.customer_id}' already exists."
            )
        return self.repo.create(CustomerModel(**dto.model_dump()))

    # --- TICKETS ---
    def list_tickets(self, skip: int, limit: int):
        return self.repo.get_all(TicketModel, skip, limit)

    def create_ticket(self, dto: TicketCreate):
        customer = self.repo.get_by_id(CustomerModel, "customer_id", dto.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer '{dto.customer_id}' not found."
            )
        return self.repo.create(TicketModel(**dto.model_dump()))

    # --- ORDERS ---
    def list_orders(self, skip: int, limit: int):
        return self.repo.get_all(OrderModel, skip, limit)

    def create_order(self, dto: OrderCreate):
        customer = self.repo.get_by_id(CustomerModel, "customer_id", dto.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer '{dto.customer_id}' not found."
            )
        return self.repo.create(OrderModel(**dto.model_dump()))
