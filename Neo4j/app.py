from fastapi import FastAPI
from app.api import router

app = FastAPI()

# Include the router from app/api.py
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    # Perform any startup tasks here if needed
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Perform any cleanup tasks here if needed
    pass
