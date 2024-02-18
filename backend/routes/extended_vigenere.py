from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from cipher.extended_vigen.main import encrypt, decrypt
from models.schemas import FileRequest, TextRequest

extended_vigenere_router = APIRouter(prefix="/vigenereext", tags=["Extended Vigenere"])

@extended_vigenere_router.post("/encrypt")
async def encrypt_handler(req: TextRequest):
  ciphertext = encrypt(req.inputText, req.key)
  return ciphertext

@extended_vigenere_router.post("/decrypt")
async def decrypt_handler(req: TextRequest):
  plaintext = decrypt(req.inputText, req.key)
  return plaintext

@extended_vigenere_router.post("/encrypt-file")
async def encrypt_handler(req: FileRequest = Depends()):
  plaintext_bytes = await req.file.read()
  plaintext_str = plaintext_bytes.decode("utf-8")
  
  ciphertext_str = encrypt(plaintext_str, req.key)
  ciphertext_bytes = ciphertext_str.encode("utf-8")
  
  response = StreamingResponse(
    iter([ciphertext_bytes]),
    media_type="application/octet-stream"
  )
  return response

@extended_vigenere_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  ciphertext_bytes = await req.file.read()
  ciphertext_str = ciphertext_bytes.decode("utf-8")
  
  plaintext_str = decrypt(ciphertext_str, req.key)
  plaintext_bytes = plaintext_str.encode("utf-8")
  
  response = StreamingResponse(
    iter([plaintext_bytes]),
    media_type="application/octet-stream"
  )
  return response
