import os
os.system("pip install -r requirements.txt")

import io
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import verify

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins = ["*"],
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

@app.post("/verify-id-owner/")
async def score(response:Response, id_: UploadFile = File(...), selfie: UploadFile = File(...)):
  response.headers["Access-Control-Allow-Origin"] = "*"
  with open(f"{id_.filename}", "wb") as buffer:
    buffer.write(await id_.read())
  with open(f"{selfie.filename}", "wb") as buffer:
    buffer.write(await selfie.read())
  result = verify.compare(id_.filename, selfie.filename)
  if result >  0.2:
    status = "Verified"
  else:
    status = "Not Verified

  os.remove(id_.filename)
  os.remove(selfie.filename)
  
  print(result)
  return {"score": float(result, 2), "stat": status}
