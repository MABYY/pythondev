from .. import models , schemas , utils , oauth2
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from  sqlalchemy.orm import Session
from ..database import engine , get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter( prefix='/posts',tags = ['Posts'])

## get all posts
# @router.get("/allposts",  response_model= List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), 
#                 current_user: int = Depends(oauth2.get_current_user), 
#                 limit: int = 10 ,skip: int = 0 , ## query parameters in FASTAPI http://localhost:8000/posts/allposts?limit=3
#                 search: Optional[str] = ""): ## retrive posts that contain this word on the title
#     posts = db.query(models.Post
#                 ).filter(models.Post.title.contains(search)
#                 ).limit(limit).all()

#     return  posts 

@router.get("/allposts",  response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user), 
                limit: int = 10 ,skip: int = 0 , ## query parameters in FASTAPI http://localhost:8000/posts/allposts?limit=3
                search: Optional[str] = ""): ## retrive posts that contain this word on the title

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


## get posts for a specific user that is logged in
@router.get("/",  response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),
                limit: int = 10): 

    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).all()
  
    return  posts 

@router.post("/" , status_code= status.HTTP_201_CREATED,  response_model= schemas.Post) ## change default status code
def create_posts(post: schemas.Post, 
            db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)): # --> data avlidation is handled by pydantic
    # print('current_user',current_user.email)
    # print('current_user',current_user.id)
    # new_post = models.Post( title = post.title, 
    #                         content = post.content, 
    #                         published = post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}",  response_model= schemas.PostOut)  ## PostOut schema shows the posts
def get_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): ## validate format or change it of necessary
   ## post = db.query(models.Post).filter(models.Post.id == id).first() # It does not show the votes

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                detail= f"Post with id {id} was not found")

    # if post.owner_id != current_user.id:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail="Not authorized to perform requested action")
    
    
    return post


@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}',  response_model= schemas.Post)
def update_post(id:int, updated_post:schemas.UpdatePost, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

############ 8: 27 ###############

# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='dbfastapi', user='postgres',
#                                 password='P24182512!')
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)


# my_posts= [ { 'id':1 ,
#         'title': 'new title',
#         'content': 'new content', 
#         'published' : True,
#         'rating': 5 },
#         {'id' : 2,
#         'title': 'new title 2',
#         'content': 'new content 2' ,
#         'published' : False,
#         'rating': 6}
#         ]
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# @app.get("/posts")
# def get_posts():
#     cursor.execute('''SELECT * FROM posts''')
#     my_posts = cursor.fetchall()
#     return {"data": my_posts}


# @app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     index = find_index_post(id)
    
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                 detail= f"Post with id {id} was not found")
    
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     #return {'message': 'Post was successfully deleted'}


# @app.put('/posts/{id}')
# def update_post(id:int, post:Post):
#     index = find_index_post(id)
#     print('index',index)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                 detail= f"Post with id {id} was not found")

#     post_dict = post.dict() ## convert to dictionary
#     post_dict['id'] = id ## add id key
#     my_posts[index] =  post_dict ## replace element in array of posts
#     return {'data': post_dict}


# @app.get("/posts/{id}") 
# def get_post(id:int, response : Response): ## validate format or change it of necessary
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                 detail= f"Post with id {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message":f"Post with id {id} was not found"}
#     return {"data": post}

# @app.post("/posts" , status_code= status.HTTP_201_CREATED) ## change default status code
# def create_post(new_post: Post): # --> data avlidation is handled by pydantic
#     post_dict = new_post.dict()
#     post_dict['id'] = randrange(0,1000)
#     my_posts.append(post_dict)
#     return my_posts

#def create_post(payload: dict = Body(...)):
#     return {"new_post": "title " +  payload["title"] + " content " + payload["content"] }
    # print(new_post)
    # print(new_post.dict()) # --> Convert pydantic model to dictionary


# # https://www.youtube.com/watch?v=0sOvCWFmrtA