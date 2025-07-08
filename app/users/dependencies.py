from datetime import datetime, timezone
from fastapi import Depends, Request, HTTPException, status
from jose import JWTError, jwt
from app.config import settings
from app.users.dao import UsersDAO

def get_token(request: Request):
      token = request.cookies.get('booking_access_token')
      if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='1')
      return token

async def get_current_user(token: str = Depends(get_token)):
      try:
          payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
          )


      except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='2')
    
      expire: str = payload.get('exp')
      if (not expire) or (expire < datetime.now(timezone.utc).timestamp()):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='3')
      user_id: str = payload.get('sub')
      if not user_id:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='4')

      user = await UsersDAO.find_by_id(int(user_id))
      if not user:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='5')
      
      return user 