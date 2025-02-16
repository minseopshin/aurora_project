from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, Request, Response
from db import userSQL

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/user")

# 회원가입 페이지
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    # print(loginSQL.select_all())
    return templates.TemplateResponse("signUp.html", { "request": request})

# 회원가입
@router.post("/signup", response_class=HTMLResponse)
async def createUser(request: Request, userid:str=Form(...), pwd:str=Form(...)):
    sqlResult = userSQL.createUser(userid, pwd)
    return templates.TemplateResponse("login.html", { "request": request})


# 아이디 중복체크
@router.get("/idchk")
async def idCheck(userid: str):
    sqlResult = userSQL.getUserList(userid)
    if len(sqlResult) == 0 :
        return  {"exists": ""}
    else :
        return  {"exists": "exists"}