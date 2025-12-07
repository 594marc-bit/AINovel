from pydantic import BaseModel
from typing import List, Optional

class AIRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    novel_id: Optional[int] = None
    chapter_id: Optional[int] = None

class AIResponse(BaseModel):
    content: str
    is_success: bool
    error_message: Optional[str] = None

class AIWriteRequest(BaseModel):
    novel_id: int
    previous_content: Optional[str] = None
    style_hint: Optional[str] = None
    length_hint: Optional[str] = "medium"
    chapter_id: Optional[int] = None
    # 新增续写配置选项
    use_context: bool = True  # 是否使用上下文信息
    context_depth: int = 3  # 使用的上下文章节数
    character_consistency: bool = True  # 是否保持角色一致性
    plot_continuity: bool = True  # 是否保持情节连续性
    writing_style: Optional[str] = None  # 续写风格：descriptive, dialog_heavy, action_focused等
    tone: Optional[str] = None  # 语气：humorous, serious, romantic等
    target_audience: Optional[str] = None  # 目标读者
    pov: Optional[str] = None  # 视角：first_person, third_person_limited, third_person_omniscient

class AIPolishRequest(BaseModel):
    content: str
    instruction: Optional[str] = None
    preserve_style: bool = True

class AIChatRequest(BaseModel):
    message: str
    novel_id: Optional[int] = None
    conversation_history: Optional[List[dict]] = None