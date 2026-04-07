"""
==============================================================
backend/app/main.py
==============================================================
This is the ENTRY POINT of the FastAPI backend.

When you run:  python -m uvicorn app.main:app --port 8000
Python starts here. This file:
  1. Creates the FastAPI app
  2. Registers all API route groups (auth, inventory, orders)
  3. On startup: creates DB tables + seeds the first admin user

TO ADD A NEW MODULE (e.g. "suppliers"):
  1. Create backend/app/models/supplier.py  (the DB table)
  2. Create backend/app/schemas/supplier.py (Pydantic validation)
  3. Create backend/app/routes/supplier.py  (the API endpoints)
  4. Create backend/app/services/supplier.py (business logic)
  5. Import and register the router below (see "Register routers")
==============================================================
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.base import Base, engine, SessionLocal
from app.routes.auth import router as auth_router
from app.routes.inventory import router as inventory_router
from app.routes.order import router as order_router
from app.services.auth import seed_admin

# ── Logging ───────────────────────────────────────────────────────────────────
# This makes the server print useful messages to the console.
# Change "INFO" to "DEBUG" to see every detail (useful when debugging).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Create FastAPI app ────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    # Swagger UI = interactive API documentation
    # Visit: http://your-server:8000/docs  to see and test all endpoints
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS Middleware ───────────────────────────────────────────────────────────
# CORS = Cross-Origin Resource Sharing
# Without this, the browser would block the Streamlit frontend
# from talking to the FastAPI backend (they run on different ports).
#
# allow_origins=["*"] means ANY website can call this API.
# For extra security in production, replace "*" with your actual URL:
#   allow_origins=["https://your-streamlit-app.railway.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Register API routers ──────────────────────────────────────────────────────
# Each router is a group of related endpoints.
# prefix = the URL prefix for all routes in that group
#
# After adding a new module, add its router here:
#   from app.routes.supplier import router as supplier_router
#   app.include_router(supplier_router)

app.include_router(auth_router)        # handles: /auth/login, /auth/users, /auth/me
app.include_router(inventory_router)   # handles: /inventory/ (CRUD)
app.include_router(order_router)       # handles: /orders/ (CRUD + summary)


# ── Startup event ─────────────────────────────────────────────────────────────
# This function runs ONCE when the server first starts.
# It is safe to run multiple times — create_all skips existing tables.
@app.on_event("startup")
def startup():
    logger.info("Step 1: Creating database tables if they don't exist...")

    # Import all models so SQLAlchemy knows about all tables
    # If you add a new model file, import it here too
    import app.models   # noqa: F401 — this import registers User, Inventory, Order

    # Create all tables that don't exist yet.
    # This is safe to run every time — it won't delete existing data.
    Base.metadata.create_all(bind=engine)
    logger.info("Tables are ready.")

    logger.info("Step 2: Creating default admin user if not exists...")
    db = SessionLocal()
    try:
        seed_admin(
            db,
            username=settings.FIRST_ADMIN_USERNAME,
            password=settings.FIRST_ADMIN_PASSWORD,
            email=settings.FIRST_ADMIN_EMAIL,
        )
        logger.info(f"Admin user '{settings.FIRST_ADMIN_USERNAME}' is ready.")
    finally:
        db.close()   # always close the DB connection

    logger.info("✅ Server startup complete! Visit /docs for API documentation.")


# ── Health check endpoint ─────────────────────────────────────────────────────
# Visit http://your-server:8000/health to quickly check if the server is running.
# Railway uses this to check if the deployment is healthy.
@app.get("/health", tags=["Health"])
def health():
    """Returns OK if server is running. Used by monitoring tools."""
    return {"status": "ok", "version": settings.VERSION}
