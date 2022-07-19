from typing import Optional

from sqlmodel import Field, SQLModel


class PKModel(SQLModel):
    """Base model class that adds a 'primary key' column named ``id``."""

    id: Optional[int] = Field(default=None, primary_key=True)
