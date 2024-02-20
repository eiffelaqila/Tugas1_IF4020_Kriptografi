import struct
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from cipher.extended_vigen.main import encrypt, encrypt_file, decrypt, decrypt_file
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
  plainbytes = await req.file.read()
  plainbytes = struct.unpack("c" * (len(plainbytes)), plainbytes)
  cipherbytes = encrypt_file(plainbytes, req.key)

  response = StreamingResponse(
    iter([cipherbytes]),
    media_type="application/octet-stream"
  )
  return response

@extended_vigenere_router.post("/decrypt-file")
async def decrypt_handler(req: FileRequest = Depends()):
  cipherbytes = await req.file.read()
  cipherbytes = struct.unpack("c" * (len(cipherbytes)), cipherbytes)
  plainbytes = decrypt_file(cipherbytes, req.key)

  response = StreamingResponse(
    iter([plainbytes]),
    media_type="application/octet-stream"
  )
  return response
