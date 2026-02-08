from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"

#primary_key=True will make it auto increment
#mapped_column defines the actual column
#Mapped[int] just tells the ide what type it is 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None
    )
#one to many rs 
#back_populates links to the author field on the post 
    posts: Mapped[list[Post]] = relationship(back_populates="author")

#if userr got image then use that image if not then use default
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        #adding an index helps the database to find it faster, need to add this manually only added automatically for primary keys
        index=True
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        #default gets called at the creation of each post so it will set the date_posted to now
        default=lambda: datetime.now(UTC),
    )

    #doing this allows you to call post.author and get all the user info, sqlalchemy does the join for us 
    author: Mapped[User] = relationship(back_populates="posts")
    


