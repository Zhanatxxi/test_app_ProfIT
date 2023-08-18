from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int
    email: EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(title="Пароль пользователя", max_length=128, min_length=8)


class UserInDB(UserBase):
    class Config:
        orm_mode = True


class LoginSchema(UserCreateSchema):
    pass


class AccessTokenSchema(BaseModel):
    access_token: str


class UserTokensSchema(AccessTokenSchema):
    email: EmailStr
    refresh_token: str

