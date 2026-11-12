from typing import Literal

from pydantic import BaseModel, Field


class Ticket(BaseModel):
    """What we want back for each support message."""

    category: Literal["billing", "bug", "question", "feature"]
    priority: int = Field(ge=1, le=5)
    summary: str = Field(min_length=5, max_length=60)
    needs_human: bool
