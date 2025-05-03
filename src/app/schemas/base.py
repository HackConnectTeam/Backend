from pydantic import BaseModel


class Base64ImageRequest(BaseModel):
    image_base64: str
