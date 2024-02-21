from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse

from cipher.enigma.main import enigma
from models.schemas import EnigmaFileRequest, EnigmaTextRequest

enigma_router = APIRouter(prefix="/enigma", tags=["Enigma"])

@enigma_router.post("/encrypt")
async def encrypt_handler(req: EnigmaTextRequest):
  try:
    ciphertext = enigma(
      req.inputText,
      req.reflector,
      [req.rotor1, req.rotor2, req.rotor3],
      [req.ring1, req.ring2, req.ring3],
      [req.position1, req.position2, req.position3],
      req.pairs,
    )
    return ciphertext

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@enigma_router.post("/decrypt")
async def decrypt_handler(req: EnigmaTextRequest):
  try:
    plaintext = enigma(
      req.inputText,
      req.reflector,
      [req.rotor1, req.rotor2, req.rotor3],
      [req.ring1, req.ring2, req.ring3],
      [req.position1, req.position2, req.position3],
      req.pairs,
    )
    return plaintext

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@enigma_router.post("/encrypt-file")
async def encrypt_handler(req: EnigmaFileRequest = Depends()):
  try:
    plaintext_bytes = await req.file.read()
    plaintext_str = plaintext_bytes.decode("utf-8")
    
    ciphertext_str = enigma(
      plaintext_str,
      req.reflector,
      [req.rotor1, req.rotor2, req.rotor3],
      [req.ring1, req.ring2, req.ring3],
      [req.position1, req.position2, req.position3],
      req.pairs,
    )
    ciphertext_bytes = ciphertext_str.encode("utf-8")
    
    response = StreamingResponse(
      iter([ciphertext_bytes]),
      media_type="application/octet-stream"
    )
    return response

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})

@enigma_router.post("/decrypt-file")
async def decrypt_handler(req: EnigmaFileRequest = Depends()):
  try:
    ciphertext_bytes = await req.file.read()
    ciphertext_str = ciphertext_bytes.decode("utf-8")
    
    plaintext_str = enigma(
      ciphertext_str,
      req.reflector,
      [req.rotor1, req.rotor2, req.rotor3],
      [req.ring1, req.ring2, req.ring3],
      [req.position1, req.position2, req.position3],
      req.pairs,
    )
    plaintext_bytes = plaintext_str.encode("utf-8")
    
    response = StreamingResponse(
      iter([plaintext_bytes]),
      media_type="application/octet-stream"
    )
    return response

  except Exception as e:
    return JSONResponse(status_code=400, content={ "error": str(e)})
