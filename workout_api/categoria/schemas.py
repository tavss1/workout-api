from pydantic import Field
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema

class Categoria(BaseSchema):
    nome: Annotated[str, Field(description="Categoria", example="Scale", max_length=10)]