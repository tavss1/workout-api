from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from workout_api.configs.database import getSession


DatabaseDependency = Annotated[AsyncSession, Depends(getSession)]