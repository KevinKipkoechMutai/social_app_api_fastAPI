from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
#from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(
                models.Post, func.count(models.Vote.post_id).label("votes")).join(
                models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(
                models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    formatted_results = [
        {"post": post[0], "votes": post[1]} for post in results
    ]
    return formatted_results
    
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print("This is the create_posts algo")
    # if user_id == None:
    #     print("The dependency is faulty")
    try:
        new_post = models.Post(owner_id = current_user.id, **post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error with the server: {e}")
    return new_post 

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    fetched_post = db.query(
            models.Post, func.count(models.Vote.post_id).label("votes")
            ).join(
                models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                ).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    #print(fetched_post)
    
    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    post, votes = fetched_post
    formatted_post = {"post": post, "votes": votes}
    
    return formatted_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   post_query = db.query(models.Post).filter(models.Post.id == id)
   
   post = post_query.first()
   
   if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
   
   if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
   
   post_query.delete(synchronize_session=False)
   db.commit()
   
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()