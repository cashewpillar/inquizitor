
from os import F_OK


class QuizChoices(TableBase):
    question_id : int = fk 
    content : str = Field(max_length=50)
    is_correct : bool
    