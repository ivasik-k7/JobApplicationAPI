from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.core.hash import get_password_hash, verify_password
from app.core.models.token import Token, TokenData
from app.core.security import oauth2_scheme
from app.db.base import get_session
from app.db.models.user import User
from app.utils.tags import ApplicationTags
from app.utils.token import create_access_token, decode_access_token

router = APIRouter(tags=[ApplicationTags.auth])


def authenticate_user(session: Session, username: str, password: str):
    user = session.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=Token(access_token=access_token, token_type="bearer").model_dump(),
    )


@router.post("/register")
def register_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    db_user = session.query(User).filter(User.username == form_data.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(form_data.password)
    db_user = User(
        username=form_data.username,
        hashed_password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=TokenData(username=db_user.username).model_dump(),
    )


@router.get("/me")
async def me(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=TokenData(username=username).model_dump(),
        )
    except InvalidTokenError:
        raise credentials_exception
