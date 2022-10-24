import httpx
from fastapi import APIRouter, status, Depends, Request, HTTPException
from sqlmodel import select, Session

from app.core.config import get_app_settings
from app.db.db import get_session
from app.db.models import *

config = get_app_settings()

router = APIRouter()


@router.post('/', response_model=Notification)
async def create_notification(notification: Notification, session: Session = Depends(get_session)):
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


@router.get('/', response_model=list[Notification])
async def get_notifications(request: Request, session: Session = Depends(get_session)):
    token = request.headers.get('Authorization')
    user = session.exec(select(User).where(User.token == token)).first()
    if not user:
        async with httpx.AsyncClient(headers={'Authorization': token}) as client:
            response = await client.get(url=f'{config.AUTH_SERVICE_URL}/api/v2/web/user/user_id/')
            if response.is_error:
                raise HTTPException(status.HTTP_403_FORBIDDEN, str(response.url))
            user_id = response.json()['id']
            user = User(id=user_id, token=token)
            session.add(user)
            session.commit()
    return session.exec(select(Notification).where(Notification.user_id == user.id)).all()
