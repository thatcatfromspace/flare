from fastapi import FastAPI
from app.routers import drivers, stores, deliveries, scoring, analytics
from app.dependencies import init_models
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Flare API")


# Register lifecycle events
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    await init_models()
    logger.info("Application startup completed")


# Register routers
app.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
app.include_router(stores.router, prefix="/stores", tags=["Stores"])
app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
app.include_router(scoring.router, prefix="/scoring", tags=["Scoring"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
