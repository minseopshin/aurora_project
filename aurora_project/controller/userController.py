from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import APIRouter, Form, Request, Response
from db import userSQL
from passlib.context import CryptContext
from config import jwtConfig

SECRET_KEY = jwtConfig.SECRET_KEY
ALGORITHM = jwtConfig.SECRET_KEY

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/user")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# 회원가입 페이지
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signUp.html", { "request": request})

# 회원가입
@router.post("/signup", response_class=HTMLResponse)
async def createUser(request: Request, userid:str=Form(...), pwd:str=Form(...)):
    hash_password = bcrypt_context.hash(pwd)
    sqlResult = userSQL.createUser(userid, hash_password)
    return templates.TemplateResponse("login.html", { "request": request})


# 아이디 중복체크
@router.get("/idchk")
async def idCheck(userid: str):
    data = {"userid":userid}
    sqlResult = userSQL.getUserList(data)
    if len(sqlResult) == 0 :
        return  {"exists": ""}
    else :
        return  {"exists": "exists"}
    

@router.post("/search", response_class=HTMLResponse)
async def searchId(request: Request, search:str=Form(...), webLinkNo:int=Form(...)):
    data = {"search": search}
    sqlResult = userSQL.getUserList(data)
    return JSONResponse(content=sqlResult)