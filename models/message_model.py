from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class Task(BaseModel):
    uuid: str
    secret: str
    response: Optional[List[Dict[str, Any]]] = None