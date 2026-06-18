from fastapi import FastAPI
from app.routes.root import router as root_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.product_image import router as product_image_router


app = FastAPI(title="Gahf API")

# include all routers here
app.include_router(root_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(product_image_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}