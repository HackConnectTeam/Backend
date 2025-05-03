from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query

from src.app.crud.challenge_match import challenge_match as crud_challenge_match
from src.app.database import SessionDep
from src.app.models.challenge_match import (
    ChallengeMatchPublic,
    ChallengeMatchCreate,
    ChallengeMatchUpdate,
)

router = APIRouter(prefix="/challenge_match", tags=["challenge_match"])


@router.get("/", response_model=List[ChallengeMatchPublic])
def read_challenge_matches(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return crud_challenge_match.get_all(db=session, offset=offset, limit=limit)


@router.get("/{challenge_match_id}", response_model=ChallengeMatchPublic)
def read_challenge_match(challenge_match_id: int, session: SessionDep):
    db_challenge_match = crud_challenge_match.get(db=session, id=challenge_match_id)
    if not db_challenge_match:
        raise HTTPException(status_code=404, detail="Challenge Match not found")
    return db_challenge_match


@router.post("/", response_model=ChallengeMatchPublic)
def create_challenge_match(challenge_match: ChallengeMatchCreate, session: SessionDep):
    return crud_challenge_match.create(db=session, obj_in=challenge_match)


@router.put("/{challenge_match_id}", response_model=ChallengeMatchPublic)
def update_challenge_match(
    challenge_match_id: int,
    challenge_match_update: ChallengeMatchUpdate,
    session: SessionDep,
):
    db_challenge_match = crud_challenge_match.get(db=session, id=challenge_match_id)
    if not db_challenge_match:
        raise HTTPException(status_code=404, detail="Challenge Match not found")
    return crud_challenge_match.update(
        db=session, db_obj=db_challenge_match, obj_in=challenge_match_update
    )


@router.delete("/{challenge_match_id}", response_model=ChallengeMatchPublic)
def delete_challenge_match(challenge_match_id: int, session: SessionDep):
    db_challenge_match = crud_challenge_match.delete(db=session, id=challenge_match_id)
    if not db_challenge_match:
        raise HTTPException(status_code=404, detail="Challenge Match not found")
    return db_challenge_match
