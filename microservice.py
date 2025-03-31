import os
os.system("pip install -r requirements.txt")

import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import verify

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins = ["*"],
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

@app.post("/verify-id-owner/")
async def score(id: UploadFile = File(...), selfie: UploadFile = File(...)):
  id = await id.read()
  selfie = await selfie.read()
  score = verify.compare(id, selfie)
  return score
