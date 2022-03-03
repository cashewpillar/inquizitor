from typing import Optional

from sqlmodel import Field, SQLModel

class TableBase(SQLModel):
	id: Optional[int] = Field(default=None, primary_key=True)
