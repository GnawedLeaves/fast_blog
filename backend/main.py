

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()


posts_db = [
    {
        "id": 1,
        "title": "Top 5 Python Tips",
        "content": "Use f-strings for better readability!",
        "published": True,
        "author": "Dev_Guru"
    },
    {
        "id": 2,
        "title": "FastAPI is Awesome",
        "content": "It handles JSON conversion automatically.",
        "published": True,
        "author": "Code_Newbie"
    },
    {
        "id": 3,
        "title": "My Secret Recipe",
        "content": "It's just coffee and debugging.",
        "published": False,
        "author": "Admin"
    }
]

@app.get("/")
def home():
    return {"message": "Hello world!", "name": "qweqwqewewq!!"}


@app.get("/firstPost")
def get_posts(): 
    return f"this is the first post: {posts_db[0]["title"]}"

@app.get("/html/firstPost", response_class=HTMLResponse, include_in_schema=False)
@app.get("/html/firstPost2", response_class=HTMLResponse, include_in_schema=False)
def get_html_post(): return f"<h1>{posts_db[0]["content"]}</h1>"
