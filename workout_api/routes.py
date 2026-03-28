from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta_router
from workout_api.categoria.controller import router as categoria_router

api_router = APIRouter()

api_router.include_router(atleta_router, prefix="/atletas", tags=["atletas"])
api_router.include_router(categoria_router, prefix="/categorias", tags=["categorias"])