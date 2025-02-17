from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette import status
from fastapi import APIRouter, Form, Request, Response
from db import webLinkSQL
from jose import jwt

SECRET_KEY = "abcde"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/weblink")

def login_check(request: Request):
    token = request.cookies.get("access_token")  # 쿠키에서 JWT 가져오기
    if not token:
        return 0
    else :
        return 1


# 웹링크 리스트
@router.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def webLinkMain(request: Request):
    if not login_check(request):
        return RedirectResponse("/")
    
    sqlResult = webLinkSQL.getWebLinkList(None)
    return templates.TemplateResponse("webLinkList.html", { "request": request, "data": sqlResult})

# 웹링크 생성 페이지
@router.get("/create/page", response_class=HTMLResponse)
async def createWebLink(request: Request):
    return templates.TemplateResponse("webLinkDetail.html", { "request": request})

# 웹링크 생성 페이지
@router.post("/create", response_class=HTMLResponse)
async def createWebLink(request: Request, url:str=Form(...), name:str=Form(...), category:str=Form(...)):
    token = request.cookies.get("access_token").replace("Bearer ", "")
    userInfo = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = {"userNo": userInfo.get("userNo"), "created_by": userInfo.get("userid"), "url": url, "name":name, "category":category, "create_date": "now"}
    webLinkSQL.createWebLink(data)
    return RedirectResponse("/weblink", status_code=302)

# 웹링크 수정
# @router.get("/update", response_class=HTMLResponse)
# async def updateWebLink(request: Request, webLinkNo:int=Form(...)):
#     data = {"webLinkNo" :webLinkNo}
#     sqlResult = webLinkSQL.getWebLinkList(data)
#     return templates.TemplateResponse("webLinkDetail.html", { "request": request, "data": sqlResult[0]})

@router.post("/update", response_class=HTMLResponse)
async def updateWebLink(request: Request, webLinkNo:int=Form(...), url:str=Form(...), name:str=Form(...), category:str=Form(...)):
    data = {"url": url, "name":name, "category":category}
    webLinkSQL.updateWebLink(webLinkNo=webLinkNo, data=data)
    return RedirectResponse("/weblink", status_code=302)

@router.post("/update/page", response_class=HTMLResponse)
async def deleteWebLink(request: Request, webLinkNo:int=Form(...)):
    data = {"webLinkNo" :webLinkNo}

    sqlResult = webLinkSQL.getWebLinkList(data)
    return templates.TemplateResponse("webLinkDetail.html", { "request": request, "data": sqlResult[0]})


# 웹링크 삭제
@router.post("/delete", response_class=HTMLResponse)
async def deleteWebLink(request: Request, webLinkNo:int=Form(...)):
    sqlResult = webLinkSQL.deleteWebLink(webLinkNo=webLinkNo)
    return RedirectResponse(url="/weblink", status_code=302)

@router.post("/search", response_class=HTMLResponse)
async def searchWebLink(request: Request, search:str=Form(...)):
    data = {"search": search}
    sqlResult = webLinkSQL.getWebLinkList(data)
    return JSONResponse(content=sqlResult)