from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, Request, Response

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/weblink")

# 웹링크 리스트
@router.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def webLinkMain(request: Request):
    return templates.TemplateResponse("webLinkList.html", { "request": request})

# 웹링크 생성
@router.get("/create", response_class=HTMLResponse)
async def createWebLink(request: Request):
    return templates.TemplateResponse("webLinkDetail.html", { "request": request})

# 웹링크 수정
@router.get("/update", response_class=HTMLResponse)
async def updateWebLink(request: Request):
    return templates.TemplateResponse("webLinkDetail.html", { "request": request})

# 웹링크 삭제
@router.get("/delete", response_class=HTMLResponse)
async def deleteWebLink(request: Request):
    return RedirectResponse(url="/weblink")


@router.get("/posttest", response_class=HTMLResponse)
async def posttest(request: Request):
    return templates.TemplateResponse("posttest.html", { "request": request})

@router.post("/posttest", response_class=HTMLResponse)
async def posttest2(request: Request, posttest:str = Form(...), pwd:str = Form(...)):
    print(posttest)
    print(pwd)
    return "a"