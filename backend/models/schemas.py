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

class EnigmaTextRequest(BaseModel):
  inputText: str
  reflector: str
  rotor1: str
  rotor2: str
  rotor3: str
  ring1: str
  ring2: str
  ring3: str
  position1: str
  position2: str
  position3: str
  pairs: str

class EnigmaFileRequest(BaseModel):
  file: UploadFile = File()
  reflector: str = Form()
  rotor1: str = Form()
  rotor2: str = Form()
  rotor3: str = Form()
  ring1: str = Form()
  ring2: str = Form()
  ring3: str = Form()
  position1: str = Form()
  position2: str = Form()
  position3: str = Form()
  pairs: str = Form()
