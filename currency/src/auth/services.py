from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException, status, Depends

from passlib.context import CryptContext

from currency.db.deps import get_db_session
from currency.settings.jwt_settings import AuthJWT
from currency.src.auth.exceptions import UserNotFound, NotVerified
from currency.src.auth.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    stmt = select(User).where(User.email.like("%{}%".format(email)))
    result = await db.scalar(stmt)
    return result


async def create_user(db: AsyncSession, *, email: str, password: str) -> User:
    """
    :param db: AsyncSession
    :param email: str
    :param password: str
    :return: model.User
    """
    hash_password = get_password_hash(password)
    user = User(
        email=email,
        hash_password=hash_password,
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user


async def check_user_in_active(user: User) -> bool:
    return True if user.is_active else False


async def get_user_by_id(db: AsyncSession, *, user_id: int) -> User | None:
    stmt = select(User) \
        .where(User.id == user_id)
    result = await db.scalar(stmt)
    return result


async def require_user(
        db: AsyncSession = Depends(get_db_session),
        Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()

        user = await get_user_by_id(db, user_id=int(user_id))

        if not user:
            raise UserNotFound('User no longer exist')

        if not user.is_active:
            raise NotVerified('You are not verified')

    except Exception as e:

        error = e.__class__.__name__

        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user_id
