from typing import Optional
from uuid import UUID

from sqlalchemy import select

from workspace.entity.db_models import Db_ModelResponse


class AI_Repo:
    def __init__(self, AsyncSession):
        self.db_session = AsyncSession

    async def save_output(self, output: Db_ModelResponse) -> Db_ModelResponse:
        self.db_session.add(output)
        await self.db_session.commit()
        await self.db_session.refresh(output)
        return output

    async def delete_output(self, output: Db_ModelResponse) -> None:
        await self.db_session.delete(output)
        await self.db_session.commit()

    async def get_output_by_id(self, output_id: UUID) -> Optional[Db_ModelResponse]:
        result = await self.db_session.scalars(select(Db_ModelResponse).where(Db_ModelResponse.id == output_id))
        return result.first()

    async def create_output(self, output: Db_ModelResponse) -> Db_ModelResponse:
        self.db_session.add(output)
        await self.db_session.commit()
        await self.db_session.refresh(output)
        return output