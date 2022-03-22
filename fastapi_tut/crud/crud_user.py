from sqlmodel import Session

from typing import Dict, Any, Optional, Union

from fastapi_tut.core.security import get_password_hash, verify_password
from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
	def get_by_email(self, db:Session, *, email: str) -> Optional[User]:
		return db.query(User).filter(User.email == email).first()


	def create(self, db: Session, *, obj_in: UserCreate) -> User:
		db_obj = User(
				username=obj_in.username,
				email=obj_in.email,
				hashed_password=get_password_hash(obj_in.password),
				last_name=obj_in.last_name,
				first_name=obj_in.first_name,
				is_superuser=obj_in.is_superuser,
				is_teacher=obj_in.is_teacher,
				is_student=obj_in.is_student
				)
		return super().create(db, obj_in=db_obj)


	def update(
		self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
	) -> User:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)

		if update_data["password"]:
			hashed_password = get_password_hash(update_data["password"])
			del update_data["password"]
			update_data["hashed_password"] = hashed_password
		return super().update(db, db_obj=db_obj, obj_in=update_data)


	def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
		user = self.get_by_email(db, email=email)
		if not user:
			return None
		
		if not verify_password(password, user.hashed_password):
			return None
			
		return user

		
	def is_superuser(self, user: User) -> bool:
		return user.is_superuser

user = CRUDUser(User)