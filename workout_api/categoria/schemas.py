from pydantic import UUID4, Field
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema

class Categoria(BaseSchema):
    nome: Annotated[str, Field(description="Categoria", example="Scale", max_length=10)]

class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description="ID da categoria")]