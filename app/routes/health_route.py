from app.controllers.health_controller import health_controller
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_route():
    return health_controller()
