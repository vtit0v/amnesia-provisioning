from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from database import init_db, get_db
from models import AmneziaClient
from provisioning import ProvisioningService
import qrcode
import io
import json

app = FastAPI(title="Amnesia Provisioning")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "Amnesia provisioning service", "version": "0.1"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/provision")
def provision(db: Session = Depends(get_db)):
    hashes = ProvisioningService.generate_random_hashes()
    conf = ProvisioningService.generate_conf("", **hashes)
    
    client = AmneziaClient(
        h1=hashes['h1'],
        h2=hashes['h2'],
        h3=hashes['h3'],
        h4=hashes['h4'],
        conf_content=conf
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    
    return {
        "client_id": client.client_id,
        "status": "provisioned",
        "created_at": client.created_at.isoformat()
    }

@app.get("/conf/{client_id}")
def get_conf(client_id: str, db: Session = Depends(get_db)):
    client = db.query(AmneziaClient).filter(AmneziaClient.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if not client.is_active:
        raise HTTPException(status_code=403, detail="Client revoked")
    
    return StreamingResponse(
        io.BytesIO(client.conf_content.encode()),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={client_id}.conf"}
    )

@app.get("/qr/{client_id}")
def get_qr(client_id: str, db: Session = Depends(get_db)):
    client = db.query(AmneziaClient).filter(AmneziaClient.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    qr_data = f"https://amnesia.ravor.ru/conf/{client_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return StreamingResponse(img_bytes, media_type="image/png")

@app.delete("/revoke/{client_id}")
def revoke(client_id: str, db: Session = Depends(get_db)):
    client = db.query(AmneziaClient).filter(AmneziaClient.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.is_active = False
    db.commit()
    
    return {"status": "revoked", "client_id": client_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
