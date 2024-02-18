from fastapi import APIRouter, Depends

from cipher.playfair.main import encrypt, decrypt
from models.schemas import FileRequest, TextRequest

playfair_router = APIRouter(prefix="/playfair", tags=["Playfair"])

@playfair_router.post("/encrypt")
async def encrypt_handler(req: TextRequest):
  ciphertext = encrypt(req.inputText, req.key)
  return {
    "message": "Playfair encrypt text successful",
    "result": ciphertext
  }

@playfair_router.post("/decrypt")
async def decrypt_handler(req: TextRequest):
  plaintext = decrypt(req.inputText, req.key)
  return {
    "message": "Playfair decrypt text successful",
    "result": plaintext
  }

@playfair_router.post("/encrypt-file")
async def encrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Playfair encrypt file successful" }

@playfair_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  # TODO:
  return { "message": "Playfair decrypt file successful" }
