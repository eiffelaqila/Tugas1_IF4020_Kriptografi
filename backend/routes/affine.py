from fastapi import APIRouter, Depends

from cipher.affine.main import encrypt, decrypt
from models.schemas import AffineFileRequest, AffineTextRequest

affine_router = APIRouter(prefix="/affine", tags=["Affine"])

@affine_router.post("/encrypt")
async def encrypt_handler(req: AffineTextRequest):
  ciphertext = encrypt(req.inputText, req.keyA, req.keyB)
  return {
    "message": "Affine encrypt text successful",
    "result": ciphertext
  }

@affine_router.post("/decrypt")
async def decrypt_handler(req: AffineTextRequest):
  plaintext = decrypt(req.inputText, req.keyA, req.keyB)
  return {
    "message": "Affine decrypt text successful",
    "result": plaintext
  }

@affine_router.post("/encrypt-file")
async def encrypt_handler(req: AffineFileRequest = Depends()):
  # TODO:
  return { "message": "Affine encrypt file successful" }

@affine_router.post("/decrypt-file")
async def decrypt_handler(req: AffineFileRequest = Depends()):
  # TODO:
  return { "message": "Affine decrypt file successful" }
