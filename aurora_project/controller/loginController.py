from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from starlette import status
from db import loginSQL

SECRET_KEY = "abcde"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/login")
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def create_access_token(userNo: int,userid: str, expires_delta: Optional[timedelta] = None):
    encode = {"userNo":userNo, "userid": userid}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(userid:str, pwd:str):
    data = {"userid": userid}
    user = loginSQL.getUserList(data=data)
    if len(user) == 0 :
        return False
    if not user[0] or not verify_password(pwd, user[0]["password"]):
        return False
    return user[0]

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(userNo= user["userNo"],userid=user["userId"])
    return {"access_token": access_token, "token_type": "bearer"}

# 로그인 페이지
@router.get("/", response_class=HTMLResponse)
async def loginMain(request: Request):
    return templates.TemplateResponse("login.html", { "request": request})

# 로그인
@router.post("/signin", response_class=HTMLResponse)
async def signIn(request: Request, userid:str=Form(...), pwd:str=Form(...)):
    user = authenticate_user(userid, pwd)
    if not user or not bcrypt_context.verify(pwd, user["password"]):
        return RedirectResponse(url="/login?error=아이디+또는+비밀번호+가+틀렸습니다.", status_code=302)

    # JWT 토큰 발급
    access_token = create_access_token(userNo=user["userNo"], userid=user["userId"])
    
    # 로그인 성공 시 쿠키에 토큰 저장 & 메인 페이지로 리디렉션
    response = RedirectResponse(url="/weblink", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    
    return response

@router.get("/signout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response