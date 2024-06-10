from typing import Optional

from pydantic import BaseModel


class APIResponse(BaseModel, extra="allow"):
    success: Optional[bool] = True
    message: Optional[str] = None
    detailed_error: Optional[object] = None
    result: Optional[object] = None
    total: Optional[int] = None
    page: Optional[int] = None
    no_items: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True
