from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Earth"}

@app.get("/cat")
async def root():
    return {"message": "Hello cat"}