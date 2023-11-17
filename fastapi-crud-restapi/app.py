from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid


app = FastAPI()

posts = []

# Post Model

class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = None
    published_at: Optional[datetime] = None
    published: bool = False

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        if "id" not in data:
            data["id"] = str(uuid())
        if "created_at" not in data:
            data["created_at"] = datetime.now()
        if "published_at" not in data:
            data["published_at"] = datetime.now()
        super().__init__(**data)

    def model_dump(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at,
            "published_at": self.published_at,
            "published": self.published,
        }

@app.get('/')
def read_root():
    return {"welcome": "Welcome to my API"}

@app.get('/posts')
def get_posts():
    return [post.model_dump() for post in posts]

@app.get('/posts/{post_id}')
def get_post(post_id:str):
    for post in posts:
        if post.id == post_id:
            return post.model_dump()
    raise HTTPException(status_code=404, detail="Post Not Found")

@app.post('/posts')
def save_posts(post: Post):
    posts.append(post)
    return posts[-1].model_dump()

@app.delete('/posts/{post_id}')
def delete_post(post_id:str):
    for index,post in enumerate(posts):
        if post.id == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Post Not Found")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post.id == post_id:
            posts[index].title = updatedPost.title
            posts[index].content = updatedPost.content
            posts[index].author = updatedPost.author
            return {"message": "Post has been updated successfully"}
    raise HTTPException(status_code=404, detail="Post Not Found")
    
