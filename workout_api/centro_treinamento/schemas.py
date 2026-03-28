from pydantic import Field
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description="Nome do Centro de Treinamento", example="CT Master", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do Centro de Treinamento", example="Rua das Flores, 123", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do Centro de Treinamento", example="João Silva", max_length=30)]