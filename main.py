from fastapi import FastAPI

app = FastAPI(title="Amnesia Provisioning")

@app.get("/")
def root():
    return {"status": "Amnesia provisioning service", "version": "0.1"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
