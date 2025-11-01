from pydantic import BaseModel


class Request(BaseModel):
    email: str
    password: str


class Response(BaseModel):
    access_token: str
    token_type: str
    role: str

