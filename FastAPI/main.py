import uvicorn
from fastapi import FastAPI

from controllers import user_controller, product_controller, auth_controller
from services.db import get_db_connection

app = FastAPI()

# User routes
app.include_router(user_controller.router, prefix="/users", tags=["Users"])

# Product routes
app.include_router(product_controller.router, prefix="/products", tags=["Products"])

# Cart routes
app.include_router(product_controller.router, prefix="/cart", tags=["Cart"])

# Auth routes
app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)