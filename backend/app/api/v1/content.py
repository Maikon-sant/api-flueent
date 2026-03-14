from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse
from app.crud import content as crud_content
from app.crud import learning_path as crud_learning_path

router = APIRouter()


@router.post(
    "/",
    response_model=ContentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new content",
    description="Create a new content item for a learning path."
)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new content item with all the information:
    
    - **learning_path_id**: ID of the learning path
    - **title**: Content title
    - **description**: Content description (optional)
    - **content_type**: Type of content (video, audio, text, exercise, quiz, interactive)
    - **theme**: Content theme (business, technical, general, conversation, grammar, vocabulary)
    - **skill**: Target skill (listening, speaking, reading, writing)
    - **duration_minutes**: Duration in minutes (optional)
    - **order_index**: Order in the learning path
    - **is_mandatory**: Whether the content is mandatory
    """
    # Validate learning path exists
    learning_path = crud_learning_path.get_learning_path(db, content.learning_path_id)
    if not learning_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    return crud_content.create_content(db=db, content=content)


@router.get(
    "/",
    response_model=List[ContentResponse],
    summary="List all contents",
    description="Retrieve a list of all contents with optional filtering."
)
def list_contents(
    skip: int = 0,
    limit: int = 100,
    learning_path_id: Optional[int] = Query(None, description="Filter by learning path ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all contents with pagination and optional filters.
    """
    contents = crud_content.get_contents(
        db, skip=skip, limit=limit, learning_path_id=learning_path_id
    )
    return contents


@router.get(
    "/{content_id}",
    response_model=ContentResponse,
    summary="Get content by ID",
    description="Retrieve a specific content by its ID."
)
def get_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific content by ID.
    """
    db_content = crud_content.get_content(db, content_id=content_id)
    if db_content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return db_content


@router.put(
    "/{content_id}",
    response_model=ContentResponse,
    summary="Update content",
    description="Update an existing content's information."
)
def update_content(
    content_id: int,
    content: ContentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a content's information.
    """
    db_content = crud_content.update_content(db, content_id=content_id, content=content)
    if db_content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return db_content


@router.delete(
    "/{content_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete content",
    description="Delete a content by its ID."
)
def delete_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a content.
    """
    success = crud_content.delete_content(db, content_id=content_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return None
