from fastapi import APIRouter, Depends

from cipher.autokey_vigen.main import encrypt, decrypt
from models.schemas import FileRequest, TextRequest

autokey_vigenere_router = APIRouter(prefix="/vigenereauto", tags=["Auto-Key Vigenere"])

@autokey_vigenere_router.post("/encrypt")
async def encrypt_handler(req: TextRequest):
  ciphertext = encrypt(req.inputText, req.key)
  return {
    "message": "Auto-key vigenere encrypt text successful",
    "result": ciphertext
  }

@autokey_vigenere_router.post("/decrypt")
async def decrypt_handler(req: TextRequest):
  plaintext = decrypt(req.inputText, req.key)
  return {
    "message": "Auto-key vigenere decrypt text successful",
    "result": plaintext
  }

@autokey_vigenere_router.post("/encrypt-file")
async def encrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Auto-key vigenere encrypt file successful" }

@autokey_vigenere_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Auto-key vigenere decrypt file successful" }
