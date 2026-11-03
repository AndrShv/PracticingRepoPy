from pydantic import BaseModel


class GeneratingRequest(BaseModel):
    prompt: str
    data: dict = {"key": "value"}
