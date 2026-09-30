import uuid
import logging
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Header, Request, Response, status
from sqlalchemy.orm import Session

from src.database import engine, get_db, Base
from src.services import OperationsService
from src.schemas import (
    CustomerCreate, CustomerResponse,
    TicketCreate, TicketResponse,
    OrderCreate, OrderResponse,
    PaginatedResponse
)

# Production logging filter to inject correlation_id safely across all modules
class CorrelationIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "correlation_id"):
            record.correlation_id = "N/A"
        return True

# Configure root logging with the safety filter attached
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [CorrelationID: %(correlation_id)s] %(message)s'
)
for handler in logging.getLogger().handlers:
    handler.addFilter(CorrelationIDFilter())

logger = logging.getLogger("atlas_ops")

# Automatically create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Atlas Ops Internal Operations API",
    description="Enterprise REST API with RBAC, pagination, and persistent storage.",
    version="2.2.0"
)

# --- MIDDLEWARE: Correlation ID Tracking & Audit Logging ---
@app.middleware("http")
async def correlation_id_and_logging_middleware(request: Request, call_next):
    # Assign or inherit a tracking ID for every request
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id

    response: Response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id

    # Log any request that modifies data
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        logger.info(
            f"Mutating Request: {request.method} {request.url.path} - Status: {response.status_code}",
            extra={"correlation_id": correlation_id}
        )
    return response

# --- RBAC SECURITY DEPENDENCY ---
VALID_ROLES = {"billing_admin", "support_agent", "viewer"}

def require_roles(allowed_roles: List[str]):
    def dependency(x_user_role: Optional[str] = Header(default=None)):
        if x_user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing required authentication header 'X-User-Role'."
            )
        if x_user_role not in VALID_ROLES:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid or unconfigured role '{x_user_role}'."
            )
        if x_user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{x_user_role}' lacks required permissions for this endpoint."
            )
        return x_user_role
    return dependency


@app.get("/")
def read_root():
    return {"system": "Atlas Ops Operations Engine", "status": "active", "version": "2.2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# --- CUSTOMERS ENDPOINTS ---
@app.get("/customers", response_model=PaginatedResponse[CustomerResponse])
def list_customers(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["billing_admin", "support_agent", "viewer"]))
):
    items, total = OperationsService(db).list_customers(skip, limit)
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    dto: CustomerCreate, 
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["billing_admin"]))
):
    return OperationsService(db).create_customer(dto)

# --- SUPPORT TICKETS ENDPOINTS ---
@app.get("/tickets", response_model=PaginatedResponse[TicketResponse])
def list_tickets(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["billing_admin", "support_agent", "viewer"]))
):
    items, total = OperationsService(db).list_tickets(skip, limit)
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@app.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    dto: TicketCreate, 
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["billing_admin", "support_agent"]))
):
    return OperationsService(db).create_ticket(dto)

# --- ORDERS ENDPOINTS ---
@app.get("/orders", response_model=PaginatedResponse[OrderResponse])
def list_orders(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["billing_admin", "support_agent", "viewer"]))
):
    items, total = OperationsService(db).list_orders(skip, limit)
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    dto: OrderCreate, 
    db: Session = Depends(get_db),
    role: str = Depends(require_roles(["billing_admin"]))
):
    return OperationsService(db).create_order(dto)
