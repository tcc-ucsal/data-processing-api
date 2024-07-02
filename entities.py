from pydantic import BaseModel

class PromptText(BaseModel):
    content: str