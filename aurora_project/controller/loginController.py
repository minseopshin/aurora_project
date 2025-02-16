from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, Request, Response
from db import loginSQL

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/login")

# 로그인 페이지
@router.get("/", response_class=HTMLResponse)
async def loginMain(request: Request):
    return templates.TemplateResponse("login.html", { "request": request})

# 로그인
@router.post("/signin", response_class=HTMLResponse)
async def signIn(request: Request, userid:str=Form(...), pwd:str=Form(...)):
    sqlResult = loginSQL.getUserList(userid, pwd)
    print(sqlResult)
    if len(sqlResult) == 0 :
        return  "A"
    else :
        return RedirectResponse(url="/weblink/")
    # return templates.TemplateResponse("login.html", { "request": request})

# 로그아웃
@router.get("/signout", response_class=HTMLResponse)
async def signOut(request: Request):
    return RedirectResponse(url="/login")