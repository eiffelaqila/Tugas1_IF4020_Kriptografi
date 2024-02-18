from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.affine import affine_router
from routes.autokey_vigenere import autokey_vigenere_router
from routes.extended_vigenere import extended_vigenere_router
from routes.playfair import playfair_router
from routes.vigenere import vigenere_router

app = FastAPI(
  title = "API Tugas 1 IF4020 Kriptografi"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(affine_router)
app.include_router(autokey_vigenere_router)
app.include_router(extended_vigenere_router)
app.include_router(playfair_router)
app.include_router(vigenere_router)
