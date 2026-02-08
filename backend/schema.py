from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    # EmailStr will autovalidate that its an email str
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    # from_attributes=True allows you to read from your database model so image_path will be imported
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_file: str | None
    image_path: str


# without default values means these are required
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


# what we accept when creating new post
# pass just means it inherit PostBase
class PostCreate(PostBase):
    user_id: int


# return from api
class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    # fields that are not provided by fe
    # this id wont conflict with db one, standard practice to use "id"
    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse
