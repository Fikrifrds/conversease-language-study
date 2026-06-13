"""Exam Runner API Routes

API endpoints for candidates to take exams.
Provides exam content, navigation, and response submission.
"""
from datetime import datetime, timezone
from typing import Optional, Union

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.routes.conversation import allowed_recorded_audio_content_type
from app.db.exam_models import (
    ExamSectionModel,
    ExamItemModel,
    MediaArtifactModel,
)
from app.db.session import get_db
from app.domain.users import User
from app.services.audio_generation import (
    AudioGenerationError,
    audio_playback_url,
    s3_configured,
    upload_audio_to_s3,
)
from app.services.exam_service import ExamService
from app.services.speech_to_text import SpeechToTextError, transcribe_recorded_audio

MAX_SPEAKING_AUDIO_BYTES = 10 * 1024 * 1024

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
                stimulus_audio_url=_stimulus_playback_url(item),
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


class SpeakingAudioUploadResponse(BaseModel):
    """Result of uploading a recorded speaking answer."""
    item_id: str
    file_url: str
    playback_url: str
    audio_size: int
    transcript: Optional[str] = None


def _stimulus_playback_url(item: ExamItemModel) -> Optional[str]:
    """Resolve a playable (signed if needed) URL for generated stimulus audio."""
    if not item.stimulus_audio_url:
        return None
    metadata = (item.config_json or {}).get("audio_generation", {})
    object_key = metadata.get("object_key", "") if isinstance(metadata, dict) else ""
    return audio_playback_url(audio_url=item.stimulus_audio_url, storage_key=object_key)


def _speaking_audio_extension(content_type: Optional[str]) -> str:
    normalized = (content_type or "").split(";", 1)[0].strip().lower()
    return {
        "audio/webm": "webm",
        "video/webm": "webm",
        "audio/mp4": "m4a",
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/ogg": "ogg",
    }.get(normalized, "webm")


@router.post("/upload-audio/{session_id}", response_model=SpeakingAudioUploadResponse)
async def upload_speaking_audio(
    session_id: str,
    item_id: str = Form(...),
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a recorded speaking answer so reviewers can play it back."""
    service = ExamService(db)

    session = service.get_exam_session(session_id)
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if session.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Exam session is {session.status}, cannot upload audio"
        )
    if session.expires_at and datetime.utcnow() > session.expires_at:
        raise HTTPException(status_code=400, detail="Exam session has expired")

    item = service.get_exam_item(item_id)
    if item.exam_template_id != session.exam_template_id:
        raise HTTPException(status_code=404, detail="Item does not belong to this exam")
    if item.item_type != "audio_response":
        raise HTTPException(status_code=422, detail="Item does not accept audio answers")

    if not allowed_recorded_audio_content_type(audio.content_type):
        raise HTTPException(status_code=422, detail="unsupported_audio_content_type")

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=422, detail="audio_file_empty")
    if len(audio_bytes) > MAX_SPEAKING_AUDIO_BYTES:
        raise HTTPException(status_code=422, detail="audio_file_too_large")

    if not s3_configured():
        raise HTTPException(status_code=503, detail="audio_storage_not_configured")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    extension = _speaking_audio_extension(audio.content_type)
    object_key = (
        f"conversease/exams/responses/{session.exam_template_id}/"
        f"{session_id}/{item_id}-{timestamp}.{extension}"
    )
    try:
        file_url = upload_audio_to_s3(
            audio_bytes=audio_bytes,
            object_key=object_key,
            content_type=audio.content_type or "audio/webm",
        )
    except AudioGenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    # Best-effort transcript so reviewers can skim the answer without replaying it.
    # STT failures never block the upload.
    transcript = None
    stt_provider = None
    stt_model = None
    stt_confidence = None
    try:
        stt_result = await transcribe_recorded_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or f"speaking-{item_id}.{extension}",
            content_type=audio.content_type,
        )
        transcript = stt_result.text
        stt_provider = stt_result.transcription.provider
        stt_model = stt_result.transcription.model
        stt_confidence = stt_result.transcription.confidence
    except SpeechToTextError:
        pass

    now = datetime.utcnow()
    artifact = MediaArtifactModel(
        id=service._generate_id(),
        owner_type="exam_response",
        owner_id=session_id,
        artifact_type="speaking_response_audio",
        file_url=file_url,
        object_key=object_key,
        mime_type=(audio.content_type or "audio/webm").split(";", 1)[0].strip(),
        file_size_bytes=len(audio_bytes),
        transcript=transcript,
        stt_provider=stt_provider,
        stt_model=stt_model,
        stt_confidence=stt_confidence,
        metadata_json={
            "item_id": item_id,
            "exam_template_id": session.exam_template_id,
            "uploaded_by": current_user.id,
        },
        created_at=now,
        updated_at=now,
    )
    db.add(artifact)
    db.commit()

    return SpeakingAudioUploadResponse(
        item_id=item_id,
        file_url=file_url,
        playback_url=audio_playback_url(audio_url=file_url, storage_key=object_key),
        audio_size=len(audio_bytes),
        transcript=transcript,
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
