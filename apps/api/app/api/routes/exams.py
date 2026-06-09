"""Exam System API Routes

API endpoints for the Real Exam System.
Based on the Technical Architecture specification.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.exam_models import (
    ExamItemModel,
    ExamResultModel,
    ExamSectionModel,
    ExamSessionModel,
    ExamTemplateModel,
    ItemResponseModel,
)
from app.db.session import get_db
from app.domain.users import User
from app.services.exam_service import (
    ExamNotFoundError,
    ExamAlreadyStartedError,
    ExamAlreadySubmittedError,
    ExamExpiredError,
    ExamNotStartedError,
    ExamService,
    ExamSessionNotFoundError,
    ExamServiceError,
)

router = APIRouter(prefix="/exams", tags=["exams"])


# ============================================================================
# Request/Response Schemas
# ============================================================================

class ExamTemplateCreate(BaseModel):
    """Schema for creating an exam template."""
    code: str = Field(..., min_length=1, max_length=32)
    level_code: str = Field(..., min_length=1, max_length=16)
    title: str = Field(..., min_length=1, max_length=160)
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0)
    passing_score_percent: int = Field(default=60, ge=0, le=100)


class ExamTemplateResponse(BaseModel):
    """Schema for exam template response."""
    id: str
    code: str
    level_code: str
    title: str
    description: Optional[str]
    duration_minutes: int
    passing_score_percent: int
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamSectionCreate(BaseModel):
    """Schema for creating an exam section."""
    code: str = Field(..., min_length=1, max_length=32)
    title: str = Field(..., min_length=1, max_length=160)
    description: Optional[str] = None
    sequence_order: int = Field(..., ge=0)
    duration_minutes: int = Field(..., gt=0)
    score_weight_percent: int = Field(..., ge=0, le=100)
    item_types_allowed: list[str]


class ExamSectionResponse(BaseModel):
    """Schema for exam section response."""
    id: str
    exam_template_id: str
    code: str
    title: str
    description: Optional[str]
    sequence_order: int
    duration_minutes: int
    score_weight_percent: int
    item_types_allowed: list[str]

    class Config:
        from_attributes = True


class ExamItemCreate(BaseModel):
    """Schema for creating an exam item."""
    section_id: str
    item_type: str = Field(..., min_length=1, max_length=32)
    sequence_order: int = Field(..., ge=0)
    prompt_text: str = Field(..., min_length=1)
    score_points: int = Field(default=1, ge=1)
    stimulus_text: Optional[str] = None
    stimulus_audio_url: Optional[str] = None
    stimulus_image_url: Optional[str] = None
    options_json: Optional[dict] = None
    correct_answer: Optional[dict] = None
    rubric_criteria: Optional[dict] = None


class ExamItemResponse(BaseModel):
    """Schema for exam item response."""
    id: str
    exam_template_id: str
    section_id: str
    item_type: str
    sequence_order: int
    prompt_text: str
    score_points: int
    stimulus_text: Optional[str]
    stimulus_audio_url: Optional[str]
    stimulus_image_url: Optional[str]
    options_json: Optional[dict]
    status: str

    class Config:
        from_attributes = True


class ExamSessionCreate(BaseModel):
    """Schema for creating an exam session."""
    exam_template_id: str


class ExamSessionResponse(BaseModel):
    """Schema for exam session response."""
    id: str
    exam_template_id: str
    user_id: str
    status: str
    current_section_id: Optional[str]
    current_item_id: Optional[str]
    started_at: Optional[datetime]
    expires_at: Optional[datetime]
    submitted_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ItemResponseCreate(BaseModel):
    """Schema for creating an item response."""
    item_id: str
    section_id: str
    response_type: str
    text_response: Optional[str] = None
    selected_option_ids: Optional[list] = None
    matched_pairs: Optional[dict] = None
    file_url: Optional[str] = None
    audio_duration_seconds: Optional[float] = None
    recording_attempts: int = 0
    time_spent_seconds: Optional[int] = None


class ItemResponseResponse(BaseModel):
    """Schema for item response response."""
    id: str
    session_id: str
    item_id: str
    section_id: str
    response_type: str
    text_response: Optional[str]
    selected_option_ids: Optional[list]
    score_points_earned: Optional[int]
    is_correct: Optional[bool]
    created_at: datetime

    class Config:
        from_attributes = True


class SubmitExamResponse(BaseModel):
    """Schema for exam submission response."""
    session_id: str
    status: str
    submitted_at: datetime
    message: str = "Exam submitted successfully"


class ExamResultResponse(BaseModel):
    """Schema for exam result response."""
    id: str
    session_id: str
    total_score: int
    max_possible_score: int
    score_percent: float
    passed: bool
    section_scores_json: dict
    strengths_json: list
    weaknesses_json: list
    recommendations_json: list
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================================
# Public API Endpoints (Candidate)
# ============================================================================

@router.get("/templates/level/{level_code}", response_model=list[ExamTemplateResponse])
async def list_exam_templates_by_level(
    level_code: str,
    db: Session = Depends(get_db),
) -> list[ExamTemplateModel]:
    """List active exam templates for a specific level."""
    service = ExamService(db)
    templates = service.list_exam_templates(
        level_code=level_code,
        status="active",
    )
    return templates


@router.post("/sessions", response_model=ExamSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_session(
    request: Request,
    data: ExamSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamSessionModel:
    """Create a new exam session for the current user."""
    service = ExamService(db)
    
    # Get client info
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    try:
        session = service.create_exam_session(
            exam_template_id=data.exam_template_id,
            user_id=current_user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return session
    except ExamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ExamServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/sessions/{session_id}", response_model=ExamSessionResponse)
async def get_exam_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamSessionModel:
    """Get details of an exam session."""
    service = ExamService(db)
    
    try:
        session = service.get_exam_session(session_id)
        
        # Verify user owns this session
        if session.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this session"
            )
        
        return session
    except ExamSessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/sessions/{session_id}/start", response_model=ExamSessionResponse)
async def start_exam_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamSessionModel:
    """Start an exam session."""
    service = ExamService(db)
    
    try:
        # Verify ownership
        session = service.get_exam_session(session_id)
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this session"
            )
        
        session = service.start_exam(session_id)
        return session
    except ExamSessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ExamAlreadyStartedError, ExamAlreadySubmittedError, ExamExpiredError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sessions/{session_id}/responses", response_model=ItemResponseResponse, status_code=status.HTTP_201_CREATED)
async def save_item_response_endpoint(
    session_id: str,
    data: ItemResponseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ItemResponseModel:
    """Save a response to an exam item."""
    service = ExamService(db)
    
    try:
        # Verify ownership
        session = service.get_exam_session(session_id)
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this session"
            )
        
        # Check exam is in progress
        if session.status != "in_progress":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exam session is {session.status}, cannot save responses"
            )
        
        # Check if expired
        if session.expires_at and datetime.utcnow() > session.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam session has expired"
            )
        
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
            recording_attempts=data.recording_attempts,
            time_spent_seconds=data.time_spent_seconds,
        )
        return response
    except ExamSessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/sessions/{session_id}/submit", response_model=SubmitExamResponse)
async def submit_exam_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Submit an exam session."""
    service = ExamService(db)
    
    try:
        # Verify ownership
        session = service.get_exam_session(session_id)
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this session"
            )
        
        session = service.submit_exam(session_id)
        return {
            "session_id": session.id,
            "status": session.status,
            "submitted_at": session.submitted_at,
            "message": "Exam submitted successfully",
        }
    except ExamSessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ExamNotStartedError, ExamAlreadySubmittedError, ExamExpiredError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/sessions/{session_id}/result", response_model=ExamResultResponse)
async def get_exam_result(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamResultModel:
    """Get the result of a completed exam session."""
    service = ExamService(db)

    try:
        # Verify ownership
        session = service.get_exam_session(session_id)
        if session.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this session"
            )

        # Get result
        result = db.execute(
            select(ExamResultModel).where(ExamResultModel.session_id == session_id)
        )
        result_record = result.scalar_one_or_none()
        
        if not result_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam result not found. Make sure the exam has been submitted and scored."
            )
        
        return result_record
    except ExamSessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================================
# Admin API Endpoints
# ============================================================================

@router.post("/admin/templates", response_model=ExamTemplateResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_exam_template(
    data: ExamTemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamTemplateModel:
    """Admin: Create a new exam template."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create exam templates"
        )

    service = ExamService(db)

    # Check for duplicate code
    existing = service.get_exam_template_by_code(data.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exam template with code '{data.code}' already exists"
        )
    
    template = service.create_exam_template(
        code=data.code,
        level_code=data.level_code,
        title=data.title,
        description=data.description,
        duration_minutes=data.duration_minutes,
        passing_score_percent=data.passing_score_percent,
        created_by=current_user.email,
    )
    return template


@router.post("/admin/templates/{template_id}/sections", response_model=ExamSectionResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_exam_section(
    template_id: str,
    data: ExamSectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamSectionModel:
    """Admin: Create a new exam section."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create exam sections"
        )

    service = ExamService(db)

    try:
        section = service.create_exam_section(
            exam_template_id=template_id,
            code=data.code,
            title=data.title,
            description=data.description,
            sequence_order=data.sequence_order,
            duration_minutes=data.duration_minutes,
            score_weight_percent=data.score_weight_percent,
            item_types_allowed=data.item_types_allowed,
        )
        return section
    except ExamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/admin/templates/{template_id}/items", response_model=ExamItemResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_exam_item(
    template_id: str,
    data: ExamItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExamItemModel:
    """Admin: Create a new exam item (question)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create exam items"
        )

    service = ExamService(db)

    item = service.create_exam_item(
        exam_template_id=template_id,
        section_id=data.section_id,
        item_type=data.item_type,
        sequence_order=data.sequence_order,
        prompt_text=data.prompt_text,
        score_points=data.score_points,
        stimulus_text=data.stimulus_text,
        stimulus_audio_url=data.stimulus_audio_url,
        stimulus_image_url=data.stimulus_image_url,
        options_json=data.options_json,
        correct_answer=data.correct_answer,
        rubric_criteria=data.rubric_criteria,
    )
    return item


@router.get("/admin/templates/{template_id}/full", response_model=dict)
async def admin_get_full_exam_template(
    template_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Admin: Get full exam template with sections and items."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view full exam templates"
        )

    service = ExamService(db)

    try:
        template = service.get_exam_template(template_id)
        sections = service.get_exam_sections(template_id)

        sections_data = []
        for section in sections:
            items = service.get_exam_items(section.id)
            sections_data.append({
                "id": section.id,
                "code": section.code,
                "title": section.title,
                "description": section.description,
                "sequence_order": section.sequence_order,
                "duration_minutes": section.duration_minutes,
                "score_weight_percent": section.score_weight_percent,
                "item_types_allowed": section.item_types_allowed,
                "items": [
                    {
                        "id": item.id,
                        "item_type": item.item_type,
                        "sequence_order": item.sequence_order,
                        "prompt_text": item.prompt_text,
                        "score_points": item.score_points,
                        "stimulus_text": item.stimulus_text,
                        "stimulus_audio_url": item.stimulus_audio_url,
                        "options_json": item.options_json,
                    }
                    for item in items
                ],
            })
        
        return {
            "id": template.id,
            "code": template.code,
            "level_code": template.level_code,
            "title": template.title,
            "description": template.description,
            "duration_minutes": template.duration_minutes,
            "passing_score_percent": template.passing_score_percent,
            "status": template.status,
            "sections": sections_data,
        }
    except ExamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
