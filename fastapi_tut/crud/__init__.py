from .crud_user import user 
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
# from fastapi_tut.models.item import Item
# from fastapi_tut.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
