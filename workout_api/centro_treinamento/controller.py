from uuid import uuid4

from fastapi import APIRouter, Body, status, HTTPException
from fastapi_pagination import Page, paginate
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamento, CentroTreinamentoOut
from workout_api.contrib.repository.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
      path="/", 
      summary="Cria um novo centro de treinamento", 
      status_code=status.HTTP_201_CREATED, 
      response_model=CentroTreinamentoOut
)

async def post(
   db_session: DatabaseDependency, 
   ct_in: CentroTreinamento = Body(...)
) -> CentroTreinamentoOut:
   
   ct_out = CentroTreinamentoOut(id=uuid4(), **ct_in.model_dump())
   ct_model = CentroTreinamentoModel(**ct_out.model_dump())

   db_session.add(ct_model)
   await db_session.commit()

   return ct_out

@router.get(
      path="/", 
      summary="Lista todos os centros de treinamento", 
      status_code=status.HTTP_200_OK, 
      response_model=Page[CentroTreinamentoOut]
)

async def query(
   db_session: DatabaseDependency
) -> Page[CentroTreinamentoOut]:
   centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
   
   return paginate([CentroTreinamentoOut.model_validate(ct) for ct in centros_treinamento])


@router.get(
      path="/{id}", 
      summary="Lista centro de treinamento por id", 
      status_code=status.HTTP_200_OK, 
      response_model=CentroTreinamentoOut
)

async def query(id: UUID4, 
   db_session: DatabaseDependency
) -> CentroTreinamentoOut:
   ct: CentroTreinamentoOut = (await db_session.execute(
      select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
   
   if not ct:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado pelo id: {id}")
   
   return ct