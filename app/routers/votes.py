from fastapi import APIRouter, Depends, status, HTTPException, Response
from  sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter( prefix='/votes',tags = ['Votes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote( vote: schemas.Vote, 
    db: Session =(Depends(database.get_db)),
    current_user: int = Depends(oauth2.get_current_user)
    ):
   
   ## Check if the post referenced exists 
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")

    ## Retrieve the post and the number of likes by the current user 
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    # Check if it is correct to add a new vote

    if (vote.dir == 1): # current vot was increased by one
        if found_vote: # the user already voted for this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        ## if not previous vote was found...
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit() 
        return {"message": "successfully added vote"}
    else:
        if not found_vote: ## you can't delete a vote that does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        # if vote found ...
        vote_query.delete(synchronize_session=False)
        db.commit() # delete and save changes
        return {"message": "successfully deleted vote"}

# https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/