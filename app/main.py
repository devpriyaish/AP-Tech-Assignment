import uvicorn
from fastapi import FastAPI
from router import auth_router

app = FastAPI()

# Include the auth router
app.include_router(auth_router)


# Test for start of the app
@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)