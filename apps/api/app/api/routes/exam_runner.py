"""Exam Runner API Routes

API endpoints for candidates to take exams.
Provides exam content, navigation, and response submission.
"""
from datetime import datetime
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.exam_models import (
    ExamSectionModel,
    ExamItemModel,
)
from app.db.session import get_db
from app.domain.users import User
from app.services.exam_service import ExamService

router = APIRouter(prefix="/exam-runner", tags=["exam-runner"])


# ============================================================================
# Request/Response Schemas
# ============================================================================

class StartExamRequest(BaseModel):
    """Request to start an exam."""
    exam_template_id: str


class ExamSessionStartResponse(BaseModel):
    """Response when starting an exam."""
    session_id: str
    exam_template_id: str
    status: str
    started_at: datetime
    expires_at: datetime
    time_remaining_seconds: int
    current_section_id: Optional[str] = None
    current_item_id: Optional[str] = None


class SectionResponse(BaseModel):
    """Section data without items."""
    id: str
    code: str
    title: str
    description: Optional[str]
    sequence_order: int
    duration_minutes: int


class ItemOption(BaseModel):
    """Option for MCQ items."""
    id: str
    text: str


class ItemResponse(BaseModel):
    """Item data for exam."""
    id: str
    item_type: str
    sequence_order: int
    prompt_text: str
    stimulus_text: Optional[str] = None
    stimulus_audio_url: Optional[str] = None
    stimulus_image_url: Optional[str] = None
    options: Optional[list[ItemOption]] = None
    options_data: Optional[Union[dict, list]] = None
    score_points: int


class ExamContentResponse(BaseModel):
    """Full exam content for a section."""
    session_id: str
    section: SectionResponse
    items: list[ItemResponse]
    total_sections: int
    current_section_number: int


class SubmitResponseRequest(BaseModel):
    """Request to submit a response."""
    item_id: str
    section_id: str
    response_type: str
    text_response: Optional[str] = None
    selected_option_ids: Optional[list[str]] = None
    matched_pairs: Optional[dict] = None
    file_url: Optional[str] = None
    audio_duration_seconds: Optional[float] = None
    time_spent_seconds: Optional[int] = None


class SubmitResponseResult(BaseModel):
    """Response submission result."""
    response_id: str
    item_id: str
    status: str = "saved"
    message: str = "Response saved successfully"


class ExamStatusResponse(BaseModel):
    """Current exam status."""
    session_id: str
    status: str
    started_at: Optional[datetime]
    expires_at: Optional[datetime]
    submitted_at: Optional[datetime]
    time_remaining_seconds: Optional[int]
    progress: dict  # section_id -> {total_items, completed_items}


class ExamManifestSection(BaseModel):
    id: str
    code: str
    title: str
    description: Optional[str]
    sequence_order: int
    duration_minutes: int


class ExamManifestResponse(BaseModel):
    session_id: str
    exam_template_id: str
    status: str
    current_section_id: Optional[str]
    current_item_id: Optional[str]
    sections: list[ExamManifestSection]


class NavigationRequest(BaseModel):
    """Request to navigate to a specific section or item."""
    target_section_id: Optional[str] = None
    target_item_id: Optional[str] = None


class NavigationResponse(BaseModel):
    """Navigation response."""
    session_id: str
    current_section_id: Optional[str]
    current_item_id: Optional[str]
    message: str


# ============================================================================
# Exam Runner Endpoints
# ============================================================================

@router.post("/start", response_model=ExamSessionStartResponse)
async def start_exam(
    data: StartExamRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Start a new exam session."""
    service = ExamService(db)
    
    # Get client info
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    # Create session
    session = service.create_exam_session(
        exam_template_id=data.exam_template_id,
        user_id=current_user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Get first section and item
    sections = service.get_exam_sections(data.exam_template_id)
    first_section_id = sections[0].id if sections else None
    
    first_item_id = None
    if first_section_id:
        items = service.get_exam_items(first_section_id)
        first_item_id = items[0].id if items else None
    
    # Start the exam
    session = service.start_exam(
        session_id=session.id,
        current_section_id=first_section_id,
        current_item_id=first_item_id,
    )
    
    # Calculate time remaining
    time_remaining = int((session.expires_at - datetime.utcnow()).total_seconds())
    
    return ExamSessionStartResponse(
        session_id=session.id,
        exam_template_id=session.exam_template_id,
        status=session.status,
        started_at=session.started_at,
        expires_at=session.expires_at,
        time_remaining_seconds=max(0, time_remaining),
        current_section_id=session.current_section_id,
        current_item_id=session.current_item_id,
    )


@router.get("/content/{session_id}/{section_id}", response_model=ExamContentResponse)
async def get_section_content(
    session_id: str,
    section_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get exam content for a specific section."""
    service = ExamService(db)
    
    # Verify session ownership
    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get section
    result = db.execute(
        select(ExamSectionModel).where(ExamSectionModel.id == section_id)
    )
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Get items
    items = service.get_exam_items(section_id)
    
    # Get total sections count
    sections_result = db.execute(
        select(ExamSectionModel)
        .where(ExamSectionModel.exam_template_id == session.exam_template_id)
        .order_by(ExamSectionModel.sequence_order)
    )
    all_sections = sections_result.scalars().all()
    current_section_number = next(
        (i + 1 for i, s in enumerate(all_sections) if s.id == section_id), 1
    )
    
    return ExamContentResponse(
        session_id=session_id,
        section=SectionResponse(
            id=section.id,
            code=section.code,
            title=section.title,
            description=section.description,
            sequence_order=section.sequence_order,
            duration_minutes=section.duration_minutes,
        ),
        items=[
            ItemResponse(
                id=item.id,
                item_type=item.item_type,
                sequence_order=item.sequence_order,
                prompt_text=item.prompt_text,
                stimulus_text=item.stimulus_text,
                stimulus_audio_url=item.stimulus_audio_url,
                stimulus_image_url=item.stimulus_image_url,
                options=[
                    ItemOption(id=opt["id"], text=opt["text"])
                    for opt in (item.options_json or [])
                ] if item.options_json and isinstance(item.options_json, list) else None,
                options_data=item.options_json,
                score_points=item.score_points,
            )
            for item in items
        ],
        total_sections=len(all_sections),
        current_section_number=current_section_number,
    )


@router.get("/manifest/{session_id}", response_model=ExamManifestResponse)
async def get_exam_manifest(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get ordered section metadata for the active exam session."""
    service = ExamService(db)

    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    sections = service.get_exam_sections(session.exam_template_id)
    return ExamManifestResponse(
        session_id=session.id,
        exam_template_id=session.exam_template_id,
        status=session.status,
        current_section_id=session.current_section_id,
        current_item_id=session.current_item_id,
        sections=[
            ExamManifestSection(
                id=section.id,
                code=section.code,
                title=section.title,
                description=section.description,
                sequence_order=section.sequence_order,
                duration_minutes=section.duration_minutes,
            )
            for section in sections
        ],
    )


@router.post("/respond/{session_id}", response_model=SubmitResponseResult)
async def submit_response(
    session_id: str,
    data: SubmitResponseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit a response for an exam item."""
    service = ExamService(db)
    
    # Verify session ownership
    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check exam is in progress
    if session.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Exam session is {session.status}, cannot submit responses"
        )
    
    # Check if expired
    if session.expires_at and datetime.utcnow() > session.expires_at:
        raise HTTPException(status_code=400, detail="Exam session has expired")
    
    # Save response
    response = service.save_item_response(
        session_id=session_id,
        item_id=data.item_id,
        section_id=data.section_id,
        response_type=data.response_type,
        text_response=data.text_response,
        selected_option_ids=data.selected_option_ids,
        matched_pairs=data.matched_pairs,
        file_url=data.file_url,
        audio_duration_seconds=data.audio_duration_seconds,
        time_spent_seconds=data.time_spent_seconds,
    )
    
    return SubmitResponseResult(
        response_id=response.id,
        item_id=response.item_id,
        status="saved",
        message="Response saved successfully",
    )


@router.post("/navigate/{session_id}", response_model=NavigationResponse)
async def navigate(
    session_id: str,
    data: NavigationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Navigate to a specific section or item."""
    service = ExamService(db)
    
    # Verify session ownership
    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update session navigation state
    session.current_section_id = data.target_section_id or session.current_section_id
    session.current_item_id = data.target_item_id or session.current_item_id
    session.updated_at = datetime.utcnow()
    db.commit()
    
    return NavigationResponse(
        session_id=session_id,
        current_section_id=session.current_section_id,
        current_item_id=session.current_item_id,
        message="Navigation successful",
    )


@router.get("/status/{session_id}", response_model=ExamStatusResponse)
async def get_exam_status(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current exam status and progress."""
    service = ExamService(db)
    
    # Verify session ownership
    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Calculate time remaining
    time_remaining = None
    if session.expires_at and session.status == "in_progress":
        time_remaining = int((session.expires_at - datetime.utcnow()).total_seconds())
        time_remaining = max(0, time_remaining)
    
    # Get progress by section
    responses = service.get_session_responses(session_id)
    completed_items = {r.item_id for r in responses}
    
    # Get all sections and items for this exam
    sections_result = db.execute(
        select(ExamSectionModel)
        .where(ExamSectionModel.exam_template_id == session.exam_template_id)
    )
    sections = sections_result.scalars().all()
    
    progress = {}
    for section in sections:
        items_result = db.execute(
            select(ExamItemModel).where(ExamItemModel.section_id == section.id)
        )
        items = items_result.scalars().all()
        total = len(items)
        completed = sum(1 for item in items if item.id in completed_items)
        progress[section.id] = {
            "total_items": total,
            "completed_items": completed,
            "section_code": section.code,
        }
    
    return ExamStatusResponse(
        session_id=session_id,
        status=session.status,
        started_at=session.started_at,
        expires_at=session.expires_at,
        submitted_at=session.submitted_at,
        time_remaining_seconds=time_remaining,
        progress=progress,
    )


@router.post("/submit/{session_id}")
async def submit_exam(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit the exam."""
    service = ExamService(db)
    
    # Verify session ownership
    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Submit exam, grade objective items, and queue subjective ones for review
    session = service.submit_exam(session_id)
    result = service.finalize_submission(session_id)

    return {
        "session_id": session_id,
        "status": session.status,
        "submitted_at": session.submitted_at,
        "result_status": result.status,
        "score_percent": result.score_percent,
        "passed": result.passed,
        "pending_review_count": (result.metadata_json or {}).get("pending_review_count", 0),
        "message": "Exam submitted successfully",
    }
