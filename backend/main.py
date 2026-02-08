# Depends will dependency injection into routes
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from schema import PostCreate, PostResponse, UserResponse, UserCreate
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Fastapi patten for type dependencies
from typing import Annotated


# select is for db
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

# create db tables: looks at models that inherit from base and creates tables if they dont already exist (safe to run  multiple times: idempotent)
Base.metadata.create_all(bind=engine)

app = FastAPI()

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


# validation
@app.get("/api/post/{post_id}", include_in_schema=False)
def get_validation_post(post_id: int):
    for post in posts_db:
        if post.get("id") == post_id:
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!!!!"
    )


# adding types
# list[PostResponse] means a list of postresponses like PostResponse[]
@app.get("/api/type/posts", response_model=list[PostResponse], include_in_schema=False)
def get_posts_w_type():
    return posts_db


@app.get(
    "/api/type/post/{post_id}", response_model=PostResponse, include_in_schema=False
)
def get_post_w_type(post_id: int):
    for post in posts_db:
        if post.get("id") == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="NO SUCH POST EXISTS HELLLO"
    )


# create posts old
@app.post(
    "/api/old/post",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts_db) + 1 if posts_db else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "7 Feb 2025",
    }
    posts_db.append(new_post)
    return new_post


# DATABASE #########################################################################
# get user by id from db
@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found!!"
    )


# user creation
@app.post(
    "/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)

# before runnign func call getdb and pass result as db in args, will be cleaned up after query due to what we defined it in database.py
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):

    # check if username exists
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    # gets the first user obj or none if no match
    existing_user = result.scalars().first()

    # db already has a constraint so stops it before it hits db
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists!!!",
        )

    # check if email exists
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists hehe"
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
    )

    db.add(new_user)
    db.commit()
    # not neccessary coz sqlalchemy will do it for you
    db.refresh(new_user)

    # pydantic will auto convvert to Userresponse
    return new_user


# get user posts
@app.get("/api/getUserPosts/{user_id}", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return posts


# get all posts
@app.get("/api/allPosts", response_model=list[PostResponse])
def get_all_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts


# get all users
@app.get("/api/allUsers", response_model=list[UserResponse])
def get_all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users


# create post
@app.post(
    "/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    new_post = models.Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
