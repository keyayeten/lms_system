from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
