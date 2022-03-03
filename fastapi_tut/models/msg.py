from sqlmodel import SQLModel

class Msg(SQLModel):
	msg: str