#!/usr/bin/env python3
# -------------------------------------------------------
# src/main.py
# -------------------------------------------------------
# Purpose Summary:
#   - Public-safe FastAPI demo for cfo-vessel-2.0 (LLM engine placeholder).
#   - Exposes /api/healthz and /api/infer endpoints.
#   - Returns a canned response; no model binaries or providers used.
# Audit:
#   - All actions print ISO 8601 UTC timestamps.
#   - Fails safe with 4xx/5xx and never exposes internal details.
# -------------------------------------------------------

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
import os

def ts() -> str:
    return datetime.now(timezone.utc).isoformat()

app = FastAPI(title="cfo-vessel-demo", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

class InferRequest(BaseModel):
    prompt: str

@app.get("/api/healthz")
def healthz():
    print(f"[{ts()}] HEALTHZ ok")
    return {"status": "ok"}

@app.post("/api/infer")
def infer(req: InferRequest = Body(...)):
    prompt_text = (req.prompt or "").strip()
    print(f"[{ts()}] INFER recv_len={len(prompt_text)}")
    if not prompt_text:
        raise HTTPException(status_code=400, detail="prompt required")
    return {
        "output": f"(demo) Generated response for: {prompt_text}",
        "meta": {"engine": "cfo-vessel-demo", "ts": ts()}
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("VESSEL_BIND", "0.0.0.0")
    port = int(os.getenv("VESSEL_PORT", "8000"))
    print(f"[{ts()}] starting cfo-vessel-demo on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
