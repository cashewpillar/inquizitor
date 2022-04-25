from sqlmodel import Session
from fastapi import Depends

from inquizitor import models
from inquizitor.api import deps

class CRUDToken:
    def revoke_access(self, authorize, db: Session):
        
        jti = authorize.get_raw_jwt()['jti']
        db_obj = models.RevokedToken(jti=jti)
        
        # TODO add the default token expiry (see core.config)
        # to remove token from denylist automatically
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def revoke_refresh(self, authorize, db: Session):
        
        jti = authorize.get_raw_jwt()['jti']
        db_obj = models.RevokedToken(jti=jti)
        
        # TODO add the default token expiry (see core.config)
        # to remove token from denylist automatically
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

token = CRUDToken()