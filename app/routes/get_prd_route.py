from app.controllers.get_prd_controller import get_prd_controller
from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.post("/get_prd")
async def get_prd_route(request: Request, response: Response):

    body = await request.json()
    project_id =  body.get("project_id")
    if not project_id:
        response.status_code = 400
        return {"error": "Missing project_id in request body"}

    generated_prd = await get_prd_controller(project_id)
    if not generated_prd:
        response.status_code = 404
        return {"error": "PRD not found for project_id"}

    return {"generated_prd": generated_prd}
