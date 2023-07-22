from .. import models, schemas, oauth2
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.PostOut])
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int =0, search: Optional[str] = ""):
    # posts = db.execute("SELECT * FROM posts").fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query = '''INSERT INTO posts (title, content, published) VALUES (:title, :content, :published)'''
    # db.execute(query, {"title": post.title, "content": post.content, "published": post.published})
    # db.commit()
    #
    # # Get the id of the newly created post
    # db_id = db.execute("SELECT LAST_INSERT_ID()").fetchone()[0]
    #
    # # Fetch the post from the database
    # post = db.execute("SELECT * FROM posts WHERE id = :id", {"id": db_id}).fetchone()

    # post = models.Post(title=post.title, content=post.content, published=post.published)

    post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.execute("SELECT * FROM posts WHERE id = :id", {"id": id}).fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with this id: {id} was not found")

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.id == id).first()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exist")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this "
    #                                                                       "action")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # try:
    #     query = '''DELETE FROM posts WHERE id = :id'''
    #     db.execute(query, {"id": id})
    #     db.commit()
    # except Exception as error:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exist")

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this "
                                                                          "action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post_: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query = '''UPDATE posts SET title = :title, content = :content, published = :published WHERE id = :id'''
    # db.execute(query, {"title": post.title, "content": post.content, "published": post.published, "id": id})
    # db.commit()
    #
    # # Fetch the post from the database
    # post = db.execute("SELECT * FROM posts WHERE id = :id", {"id": id}).fetchone()

    db.query(models.Post).filter(models.Post.id == id).update(post_.dict(), synchronize_session=False)
    db.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this "
                                                                          "action")

    return post
