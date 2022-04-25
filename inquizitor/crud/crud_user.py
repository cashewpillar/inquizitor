from sqlmodel import select, Session

from typing import Dict, Any, Optional, Union

from inquizitor.core.security import get_password_hash, verify_password
from inquizitor.crud.base import CRUDBase
from inquizitor.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
	def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
		return db.query(User).filter(User.email == email).first()

	def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
		return db.query(User).filter(User.username == username).first()

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

	def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
		user = self.get_by_username(db, username=username)
		if not user:
			return None
		
		if not verify_password(password, user.hashed_password):
			return None
			
		return user
		
	def is_superuser(self, user: User) -> bool:
		return user.is_superuser

	def is_student(self, user: User) -> bool:
		return user.is_student

	def is_teacher(self, user: User) -> bool:
		return user.is_teacher

user = CRUDUser(User)