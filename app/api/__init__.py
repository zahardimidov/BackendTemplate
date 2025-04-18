from fastapi import APIRouter, Response
from fastapi.routing import APIRoute
from app.api.users import router as users_router


router = APIRouter(prefix='/api')

@router.get('/ping')
async def ping():
    return Response(status_code=200)

router.include_router(users_router)


for route in router.routes:
    if isinstance(route, APIRoute):
        route.response_model_exclude_none = True
        parts = route.name.split("_")
        route.operation_id = "".join(map(str.capitalize, parts))
