from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from schema import PostCreate, PostResponse

app = FastAPI()


posts_db = [
    {
        "id": 1,
        "title": "Top 5 Python Tips",
        "content": "Use f-strings for better readability!",
        "author": "Dev_Guru",
        "date_posted": "25/10/25"
    },
    {
        "id": 2,
        "title": "FastAPI is Awesome",
        "content": "It handles JSON conversion automatically.",
        "author": "Code_Newbie",
          "date_posted": "25/10/25"
    },
    {
        "id": 3,
        "title": "My Secret Recipe",
        "content": "It's just coffee and debugging.",
        "author": "Admin",
          "date_posted": "25/10/25"
    }
]

@app.get("/")
def home():
    return {"message": "Hello world!", "name": "qweqwqewewq!!"}


@app.get("/firstPost")
def get_posts(): 
    return f"this is the first post: {posts_db[0]["title"]}"

# returning html
@app.get("/html/firstPost", response_class=HTMLResponse, include_in_schema=False)
@app.get("/html/firstPost2", response_class=HTMLResponse, include_in_schema=False)
def get_html_post(): return f"<h1>{posts_db[0]["content"]}</h1>"


# validation
@app.get("/api/post/{post_id}")
def get_validation_post(post_id: int):
    for post in posts_db: 
        if post.get("id") == post_id:
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!!!!")

#adding types
#list[PostResponse] means a list of postresponses like PostResponse[]
@app.get("/api/type/posts", response_model=list[PostResponse])
def get_posts_w_type(): 
    return posts_db

@app.get("/api/type/post/{post_id}",response_model=PostResponse)
def get_post_w_type(post_id: int):
    for post in posts_db:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO SUCH POST EXISTS HELLLO") 
    
#create posts
@app.post("/api/post",response_model=PostResponse,
          status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts_db) + 1 if posts_db else 1 
    new_post ={ 
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "7 Feb 2025"
    }
    posts_db.append(new_post)
    return new_post
    
