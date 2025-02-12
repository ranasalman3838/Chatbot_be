from typing import TypedDict, List, Optional, Dict, Any


class State(TypedDict):
    text: str
    classification: Optional[str]
    entities: List[str]
    summary: str
    error: Optional[str]
    metadata: Dict[str, Any]