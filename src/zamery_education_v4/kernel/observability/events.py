from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

EventType = Literal["RUN_PLANNED","NODE_READY","CACHE_HIT","CAPABILITY_STARTED","CAPABILITY_COMPLETED","OUTPUT_REJECTED","REVIEW_REQUIRED","GATE_DECIDED","REPAIR_PLANNED","BUNDLE_PUBLISHED"]
class RunEvent(BaseModel):
    model_config=ConfigDict(extra="forbid", frozen=True, strict=True)
    event_type: EventType
    run_id: str
    data: dict[str, object]=Field(default_factory=dict)
    occurred_at: datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
