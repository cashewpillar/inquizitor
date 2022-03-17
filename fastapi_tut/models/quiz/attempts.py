
from os import F_OK


class QuizAttempts(TableBase):
    is_done : Optional[bool] = False
    quiz_id : int = fk
    recent_question_id : int = fk
    student_id : int = fk
