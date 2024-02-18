from pydantic import BaseModel
from fastapi import File, Form, UploadFile

class TextRequest(BaseModel):
  inputText: str
  key: str

class FileRequest(BaseModel):
  file: UploadFile = File()
  key: str = Form()

class AffineTextRequest(BaseModel):
  inputText: str
  keyA: int
  keyB: int

class AffineFileRequest(BaseModel):
  file: UploadFile = File()
  keyA: int = Form()
  keyB: int = Form()
