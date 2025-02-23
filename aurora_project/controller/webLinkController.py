from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import APIRouter, Form, Request
from db import webLinkSQL
from jose import jwt
from config import jwtConfig

SECRET_KEY = jwtConfig.SECRET_KEY
ALGORITHM = jwtConfig.SECRET_KEY

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/weblink")


# 웹링크 리스트
@router.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def webLinkMain(request: Request):

    token = request.cookies.get("access_token").replace("Bearer ", "")
    userInfo = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = {"shareUserNo": userInfo.get("userNo")}
    sqlResult = webLinkSQL.getWebLinkList(data)
    return templates.TemplateResponse("webLinkList.html", { "request": request, "data": sqlResult})

# 웹링크 생성 페이지
@router.get("/create/page", response_class=HTMLResponse)
async def createWebLink(request: Request):
    return templates.TemplateResponse("webLinkDetail.html", { "request": request, "mode": "생성"})

# 웹링크 생성 페이지
@router.post("/create", response_class=HTMLResponse)
async def createWebLink(request: Request, url:str=Form(...), name:str=Form(...), category:str=Form(...)):
    token = request.cookies.get("access_token").replace("Bearer ", "")
    userInfo = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = {"userNo": userInfo.get("userNo"), "created_by": userInfo.get("userid"), "url": url, "name":name, "category":category}
    webLinkSQL.createWebLink(data)
    return RedirectResponse("/weblink", status_code=302)

@router.post("/update", response_class=HTMLResponse)
async def updateWebLink(request: Request, webLinkNo:int=Form(...), url:str=Form(...), name:str=Form(...), category:str=Form(...)):
    data = {"url": url, "name":name, "category":category}
    webLinkSQL.updateWebLink(webLinkNo=webLinkNo, data=data)
    return RedirectResponse("/weblink", status_code=302)

@router.post("/update/page", response_class=HTMLResponse)
async def deleteWebLink(request: Request, webLinkNo:int=Form(...)):
    data = {"webLinkNo" :webLinkNo}
    sqlResult = webLinkSQL.getWebLinkList(data)
    return templates.TemplateResponse("webLinkDetail.html", { "request": request, "data": sqlResult[0], "mode": "웹링크 수정"})


# 웹링크 삭제
@router.post("/delete", response_class=HTMLResponse)
async def deleteWebLink(request: Request, webLinkNo:int=Form(...)):
    sqlResult = webLinkSQL.deleteWebLink(webLinkNo=webLinkNo)
    return RedirectResponse(url="/weblink", status_code=302)


@router.post("/search", response_class=HTMLResponse)
async def searchWebLink(request: Request, search:str=Form(...)):
    token = request.cookies.get("access_token").replace("Bearer ", "")
    userInfo = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = {"search": search, "shareUserNo": userInfo.get("userNo")}
    sqlResult = webLinkSQL.getWebLinkList(data)
    json_data = jsonable_encoder(sqlResult)
    return JSONResponse(content=json_data)


@router.get("/share", response_class=HTMLResponse)
async def shareWebLink(request: Request):
    return templates.TemplateResponse("webLinkShare.html", { "request": request})

@router.post("/share/search", response_class=HTMLResponse)
async def searchShareWebLink(request: Request, search:str=Form(...), webLinkNo:str=Form(...)):
    token = request.cookies.get("access_token").replace("Bearer ", "")
    userInfo = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = {"search": search, "webLinkNo":webLinkNo, "userNo": userInfo.get("userNo")}
    sqlResult = webLinkSQL.getWebLinkShareUserList(data)

    return JSONResponse(content=sqlResult)


@router.post("/share")
async def shareWebLink(request: Request):
    data = await request.json()
    sqlResult = webLinkSQL.getWebLinkShareList(data)

    if len(sqlResult) == 0 :
        webLinkSQL.createWebLinkShare(data)
    else :
        webLinkSQL.updateWebLinkShare(data,sqlResult)
    
    return True