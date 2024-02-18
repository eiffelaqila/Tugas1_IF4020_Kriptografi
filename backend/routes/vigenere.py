from fastapi import APIRouter, Depends

from cipher.vigenere.main import encrypt, decrypt
from models.schemas import FileRequest, TextRequest

vigenere_router = APIRouter(prefix="/vigenere", tags=["Vigenere"])

@vigenere_router.post("/encrypt")
async def encrypt_handler(req: TextRequest):
  ciphertext = encrypt(req.inputText, req.key)
  return {
    "message": "Vigenere encrypt text successful",
    "result": ciphertext
  }

@vigenere_router.post("/decrypt")
async def decrypt_handler(req: TextRequest):
  plaintext = decrypt(req.inputText, req.key)
  return {
    "message": "Vigenere decrypt text successful",
    "result": plaintext
  }

@vigenere_router.post("/encrypt-file")
async def encrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Vigenere encrypt file successful" }

@vigenere_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Vigenere decrypt file successful" }
