from fastapi import FastAPI
from controller import loginController, webLinkController, userController

app = FastAPI()

@app.get("/") 
async def first_api(): 
  return {"message":"Hello Eric!"}

app.include_router(loginController.router)
app.include_router(webLinkController.router)
app.include_router(userController.router)