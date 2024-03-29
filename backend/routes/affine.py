from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse

from cipher.affine.main import encrypt, decrypt
from models.schemas import AffineFileRequest, AffineTextRequest

affine_router = APIRouter(prefix="/affine", tags=["Affine"])

@affine_router.post("/encrypt")
async def encrypt_handler(req: AffineTextRequest):
  try:
    ciphertext = encrypt(req.inputText, req.keyA, req.keyB)
    return ciphertext
  
  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@affine_router.post("/decrypt")
async def decrypt_handler(req: AffineTextRequest):
  try:
    plaintext = decrypt(req.inputText, req.keyA, req.keyB)
    return plaintext
  
  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@affine_router.post("/encrypt-file")
async def encrypt_handler(req: AffineFileRequest = Depends()):
  try:
    plaintext_bytes = await req.file.read()
    plaintext_str = plaintext_bytes.decode("utf-8")
    
    ciphertext_str = encrypt(plaintext_str, req.keyA, req.keyB)
    ciphertext_bytes = ciphertext_str.encode("utf-8")
    
    response = StreamingResponse(
      iter([ciphertext_bytes]),
      media_type="application/octet-stream"
    )
    return response
  
  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@affine_router.post("/decrypt-file")
async def decrypt_handler(req: AffineFileRequest = Depends()):
  try:
    ciphertext_bytes = await req.file.read()
    ciphertext_str = ciphertext_bytes.decode("utf-8")
    
    plaintext_str = decrypt(ciphertext_str, req.keyA, req.keyB)
    plaintext_bytes = plaintext_str.encode("utf-8")
    
    response = StreamingResponse(
      iter([plaintext_bytes]),
      media_type="application/octet-stream"
    )
    return response
  
  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})