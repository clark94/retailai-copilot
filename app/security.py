"""Demo bearer tokens. Production: validate Google OIDC JWT against JWKS."""
import os
from fastapi import Header, HTTPException
from pydantic import BaseModel
from typing import Optional

class Principal(BaseModel):
    role: str
    countries: list[str]
    brands: list[str]

def current_user(authorization: Optional[str] = Header(default=None)) -> Principal:
    token = os.getenv("DEMO_API_TOKEN", "")
    if not token:
        raise HTTPException(503, "Configure DEMO_API_TOKEN (secret, non vide)")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Bearer token requis")
    import hmac
    if not hmac.compare_digest(authorization[7:], token):
        raise HTTPException(403, "Token invalide")
    # Demo claims are server-side, NEVER accepted from the client.
    return Principal(
        role=os.getenv("DEMO_ROLE", "analyst"),
        countries=[v.strip() for v in os.getenv("DEMO_ALLOWED_COUNTRIES", "France").split(",") if v.strip()],
        brands=[v.strip() for v in os.getenv("DEMO_ALLOWED_BRANDS", "Casanoov,Cazeboo,Sicaan").split(",") if v.strip()],
    )
