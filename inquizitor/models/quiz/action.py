import datetime as dt
import logging
from inquizitor.db.base_class import PKModel
from pydantic import root_validator, validator
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

class QuizActionBase(SQLModel):
    # these fields are optional because they are set in the POST request 
    attempt_id: Optional[int] = Field(foreign_key="quizattempt.id")
    question_id: Optional[int] = Field(foreign_key="quizquestion.id")
    time: Optional[dt.datetime] = Field(default=dt.datetime.now())

    blur: int = Field(default=0)
    focus: int = Field(default=0)
    # NameError: Field name "copy" shadows a BaseModel attribute; use a different field name with "alias='copy'"
    copy_: int = Field(default=0)
    paste: int = Field(default=0)
    left_click: int = Field(default=0)
    right_click: int = Field(default=0)
    double_click: int = Field(default=0)

    @validator('double_click')
    def check_has_action(cls, v, values, **kwargs):
        actions = [
            values['blur'],
            values['focus'],
            values['copy_'],
            values['paste'],
            values['left_click'],
            values['right_click'],
            v, # values['double_click'],
        ]
        if sum(actions) > 1:
            raise Exception('Only a single action is allowed per record')
        elif sum(actions) < 1:
            raise Exception('Record must have an action/ event')
        return v

class QuizActionCreate(QuizActionBase):
    pass

# kept for CRUD purposes, endpoint will not be created
class QuizActionUpdate(QuizActionBase):
    blur: Optional[int] = Field(default=0)
    focus: Optional[int] = Field(default=0)
    copy_: Optional[int] = Field(default=0)
    paste: Optional[int] = Field(default=0)
    left_click: Optional[int] = Field(default=0)
    right_click: Optional[int] = Field(default=0)
    double_click: Optional[int] = Field(default=0)

class QuizActionInDBBase(QuizActionBase, PKModel):
    pass

class QuizAction(QuizActionInDBBase, table=True):
    attempt: Optional["QuizAttempt"] = Relationship(back_populates="actions")
    question: Optional["QuizQuestion"] = Relationship(back_populates="actions")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Action({self.student.username!r}-{self.time!r}) - blur={self.blur!r} focus={self.focus!r} copy={self.copy_!r} paste={self.paste!r} left_click={self.left_click!r} right_click={self.right_click!r} double_click={self.double_click!r}>"