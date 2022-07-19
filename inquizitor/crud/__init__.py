from .crud_user import user
from .crud_token import token
from .crud_quiz import (
    quiz_answer,
    quiz_attempt,
    quiz_choice,
    quiz_student_link,
    quiz_question,
    quiz,
)

# For a new basic set of CRUD operations you could do

# from .base import CRUDBase
# from inquizitor.models.item import Item
# from inquizitor.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
