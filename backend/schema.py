

from pydantic import BaseModel, ConfigDict, Field



# without default values means these are required
class PostBase(BaseModel): 
    title: str = Field(min_length=1,max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1,max_length=100)


# what we accept when creating new post
# pass just means it inherit PostBase
class PostCreate(PostBase):
    pass


# return from api
class PostResponse(PostBase):
    #fromA read data from obj with attr and not just dicts
    #eg it can read from post.title too instead of just post["title"]
    model_config = ConfigDict(from_attributes=True)

# fields that are not provided by fe
# this id wont conflict with db one, standard practice to use "id"
    id: int
    date_posted: str

