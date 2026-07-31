from fastapi import FastAPI

app = FastAPI(title="Internal Developer Portal")

@app.get("/")
def read_root():
    return {"message": "Internal Developer Portal'a Hoş Geldiniz! 🚀"}