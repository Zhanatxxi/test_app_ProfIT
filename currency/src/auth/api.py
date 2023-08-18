from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status

from currency.settings.jwt_settings import AuthJWT

from currency.db.deps import get_db_session
from currency.settings.settings import settings
from currency.src.auth import services
from currency.src.auth.models import User
from currency.src.auth.schemas import UserCreateSchema, UserInDB, LoginSchema, UserTokensSchema, AccessTokenSchema

api = APIRouter()


@api.post("/sign-up", response_model=UserInDB)
async def sign_up(
        user: UserCreateSchema,
        db: AsyncSession = Depends(get_db_session),
):
    users = await services.get_user_by_email(db, email=user.email)

    if users:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user_ins = await services.create_user(
        db,
        email=user.email,
        password=user.password,
    )

    return user_ins


@api.post("/login", response_model=UserTokensSchema)
async def login(
        user_in: LoginSchema,
        Authorize: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db_session),
):
    user: User | None = await services.get_user_by_email(db, email=user_in.email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect Email or Password"
        )

    if not services.verify_password(user_in.password, user.hash_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect Email or Password"
        )

    is_active = await services.check_user_in_active(user)
    if not is_active:
        raise HTTPException(
            status_code=400,
            detail="Please verify your email address"
        )

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(days=settings.REFRESH_TOKEN_EXPIRES_IN))

    return UserTokensSchema(
        email=user.email,
        access_token=access_token,
        refresh_token=refresh_token
    )


@api.get('/refresh', response_model=AccessTokenSchema)
async def refresh_token(
        Authorize: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db_session)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        user = await services.get_user_by_id(db, user_id=int(user_id))

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')

        access_token = Authorize.create_access_token(
            subject=str(user.id), expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN))

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return AccessTokenSchema(access_token=access_token)
