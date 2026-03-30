from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, Atleta, AtletaUpdate
from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.repository.dependencies import DatabaseDependency

router = APIRouter()

@router.post(path="/", summary="Cria um novo atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)

async def post(
   db_session: DatabaseDependency, 
   atleta_in: Atleta = Body(...)
) -> AtletaOut:
   
   categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()

   if not categoria:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A categoria {atleta_in.categoria.nome} não foi encontrada.")
   
   centros_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()

   if not centros_treinamento:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"O centro de treinamento {atleta_in.centro_treinamento.nome} não foi encontrado.")

   try:
      atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
   
      atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
      atleta_model.categoria_id = categoria.pk_id
      atleta_model.centro_treinamento_id = centros_treinamento.pk_id

      db_session.add(atleta_model)
      await db_session.commit()

   except Exception:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar o atleta. O cpf do atleta {atleta_in.cpf} já existe.")
   
   return atleta_out

@router.get(
      path="/", 
      summary="Lista todos os atletas", 
      status_code=status.HTTP_200_OK, 
      response_model=list[AtletaOut]
)

async def query(
   db_session: DatabaseDependency
) -> list[AtletaOut]:
   atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
   
   return [AtletaOut.model_validate(atleta) for atleta in atletas] 

@router.get(
      path="/{id}", 
      summary="Lista atleta por id", 
      status_code=status.HTTP_200_OK, 
      response_model=AtletaOut
)

async def query(id: UUID4, 
   db_session: DatabaseDependency
) -> AtletaOut:
   atleta: AtletaOut = (await db_session.execute(
      select(AtletaModel).filter_by(id=id))).scalars().first()
   
   if not atleta:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
   
   return atleta

# Atualizar atleta por ID -> Patch
@router.patch(
      path="/{id}", 
      summary="Atualiza um atleta por id", 
      status_code=status.HTTP_200_OK, 
      response_model=AtletaOut
)
async def patch(
   id: UUID4, 
   db_session: DatabaseDependency, 
   atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
   atleta: AtletaOut = (await db_session.execute(
      select(AtletaModel).filter_by(id=id))).scalars().first()
   
   if not atleta:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
   
   atleta_update = atleta_up.model_dump(exclude_unset=True)
   
   for key, value in atleta_update.items():
      setattr(atleta, key, value)
   
   await db_session.commit()
   await db_session.refresh(atleta)

   return atleta

@router.delete(
      path="/{id}", 
      summary="Deletar um atleta por id", 
      status_code=status.HTTP_204_NO_CONTENT, 
)

async def query(id: UUID4, 
   db_session: DatabaseDependency
) -> None:
   atleta: AtletaOut = (await db_session.execute(
      select(AtletaModel).filter_by(id=id))).scalars().first()
   
   if not atleta:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
   
   await db_session.delete(atleta)
   await db_session.commit()