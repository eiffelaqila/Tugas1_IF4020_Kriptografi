from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse

from cipher.playfair.main import encrypt, decrypt
from models.schemas import FileRequest, TextRequest

playfair_router = APIRouter(prefix="/playfair", tags=["Playfair"])

@playfair_router.post("/encrypt")
async def encrypt_handler(req: TextRequest):
  try:
    ciphertext = encrypt(req.inputText, req.key)
    return ciphertext

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@playfair_router.post("/decrypt")
async def decrypt_handler(req: TextRequest):
  try:
    plaintext = decrypt(req.inputText, req.key)
    return plaintext

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@playfair_router.post("/encrypt-file")
async def encrypt_handler(req: FileRequest = Depends()):
  try:
    plaintext_bytes = await req.file.read()
    plaintext_str = plaintext_bytes.decode("utf-8")
    
    ciphertext_str = encrypt(plaintext_str, req.key)
    ciphertext_bytes = ciphertext_str.encode("utf-8")
    
    response = StreamingResponse(
      iter([ciphertext_bytes]),
      media_type="application/octet-stream"
    )
    return response

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@playfair_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  try:
    ciphertext_bytes = await req.file.read()
    ciphertext_str = ciphertext_bytes.decode("utf-8")
    
    plaintext_str = decrypt(ciphertext_str, req.key)
    plaintext_bytes = plaintext_str.encode("utf-8")
    
    response = StreamingResponse(
      iter([plaintext_bytes]),
      media_type="application/octet-stream"
    )
    return response

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})
