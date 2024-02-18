from fastapi import APIRouter, Depends

from cipher.extended_vigen.main import encrypt, decrypt
from models.schemas import FileRequest, TextRequest

extended_vigenere_router = APIRouter(prefix="/vigenereext", tags=["Extended Vigenere"])

@extended_vigenere_router.post("/encrypt")
async def encrypt_handler(req: TextRequest):
  ciphertext = encrypt(req.inputText, req.key)
  return {
    "message": "Extended vigenere encrypt text successful",
    "result": ciphertext
  }

@extended_vigenere_router.post("/decrypt")
async def decrypt_handler(req: TextRequest):
  plaintext = decrypt(req.inputText, req.key)
  return {
    "message": "Extended vigenere decrypt text successful",
    "result": plaintext
  }

@extended_vigenere_router.post("/encrypt-file")
async def encrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Extended vigenere encrypt file successful" }

@extended_vigenere_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Extended vigenere decrypt file successful" }
