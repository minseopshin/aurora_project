from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from jose import ExpiredSignatureError
from controller import loginController, webLinkController, userController

app = FastAPI()

# 토큰 만료시 로그인페이지로 리다이렉트
@app.middleware("http")
async def expired_signature_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except ExpiredSignatureError:
        return RedirectResponse(url="/")

# 프로젝트 실행시 로그인페이지
@app.get("/") 
async def first_api(): 
  return RedirectResponse(url="/login")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(loginController.router)
app.include_router(webLinkController.router)
app.include_router(userController.router)