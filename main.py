from fastapi import FastAPI
from database import engine, Base
from routers import driver, route

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TMS API",
    description="Transportation Management System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "TMS API is running!"}

# Daftarkan semua router
app.include_router(driver.router)
app.include_router(route.router)