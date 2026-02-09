# Depends will dependency injection into routes
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from schema import (
    PostCreate,
    PostResponse,
    UserResponse,
    UserCreate,
    PostUpdate,
    UserUpdate,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Fastapi patten for type dependencies
from typing import Annotated

from contextlib import asynccontextmanager
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# select is for db
from sqlalchemy import select
from sqlalchemy.orm import Session

from starlette.exceptions import HTTPException

import models
from database import Base, engine, get_db


# @asynccontextmanager turns this into an async context manager
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # runs at startup, begin will create an async connection
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# creates a /media prefix and serves files from there
app.mount("/media", StaticFiles(directory="media"), name="media")

posts_db = []


@app.get("/", include_in_schema=False)
def home():
    return {"message": "Hello world!", "name": "qweqwqewewq!!"}


@app.get("/firstPost", include_in_schema=False)
def get_posts():
    return f"this is the first post: {posts_db[0]["title"]}"


# returning html
@app.get("/html/firstPost", response_class=HTMLResponse, include_in_schema=False)
@app.get("/html/firstPost2", response_class=HTMLResponse, include_in_schema=False)
def get_html_post():
    return f"<h1>{posts_db[0]["content"]}</h1>"


# DATABASE #########################################################################
# get user by id
@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# before runnign func call getdb and pass result as db in args, will be cleaned up after query due to what we defined it in database.py
@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.username == user.username),
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    result = await db.execute(
        select(models.User).where(models.User.email == user.email),
    )
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# get user posts
@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    # does not need selectinload because it doesnt have a rs
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id),
    )
    posts = result.scalars().all()
    return posts


# get post by id
@app.get("/api/post/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post doesnt exist!!!!"
        )
    return post


# get all posts
@app.get("/api/allPosts", response_model=list[PostResponse])
async def get_all_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post).options(selectinload(models.Post.author))
    )
    posts = result.scalars().all()
    return posts


# get all users
@app.get("/api/allUsers", response_model=list[UserResponse])
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


# create post
@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(post: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.id == post.user_id),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    await db.commit()
    # refreshes the post and fetch the author relationship
    await db.refresh(new_post, attribute_names=["author"])
    return new_post


# put
@app.put("/api/posts/{post.id}", response_model=PostResponse)
async def update_post_full(
    post_id: int, post_data: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    post_exists_res = await db.execute(
        select(models.Post).where(models.Post.id == post_id)
    )
    post = post_exists_res.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found to update!"
        )

    # check if the new user exists
    if post_data.user_id != post.user_id:
        result = db.execute(
            select(models.User).where(models.User.id == post_data.user_id)
        )
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_type=status.HTTP_404_NOT_FOUND,
                detail="User not found for update!",
            )
    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post


# patch
@app.patch("/api/posts/{post_id}", response_model=PostResponse)
async def patch_post(
    post_id: int, post_data: PostUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found FOR PATCH"
        )

    # important: returns a dictionary of what the client actually sent in. so if the user only updated "content" then it wont set title to None
    # update_data = post_data.model_dump(exclude_unset=True)
    update_data = post_data.model_dump(exclude_unset=True)

    # for post we update each field with the new value from updateData
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post


# delete post
@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no found while deleting"
        )

    await db.delete(post)
    await db.commit()


# delete user
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found for delete"
        )
    await db.delete(user)
    await db.commit()
