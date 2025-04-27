from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from starlette.middleware.sessions import SessionMiddleware
import requests
import os

app = FastAPI()

# Add secret key for sessions
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "../frontend/static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "../frontend/templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# In-memory "database"
users = {}  # {"username": "password"}
user_searches = {}  # {"username": ["car", "cat"]}

OPENVERSE_API_URL = "https://api.openverse.engineering/v1/images"

# --------------------
# Auth-related routes
# --------------------
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = password
    user_searches[username] = []
    response = RedirectResponse(url="/login", status_code=302)
    return response

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if users.get(username) != password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    request.session['username'] = username
    response = RedirectResponse(url="/", status_code=302)
    return response

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

# --------------------
# Search-related routes
# --------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    username = request.session.get('username')
    recent = user_searches.get(username, []) if username else []
    return templates.TemplateResponse("index.html", {"request": request, "recent": recent})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: Optional[str] = None):
    username = request.session.get('username')
    results = []
    if username and query:
        # Save search
        user_searches[username].append(query)
        if len(user_searches[username]) > 5:  # Keep only last 5 searches
            user_searches[username] = user_searches[username][-5:]

        try:
            params = {"q": query, "license_type": "all", "page_size": 10}
            response = requests.get(OPENVERSE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            results = [{"type": "image", "url": item["thumbnail"]} for item in data.get("results", []) if item.get("thumbnail")]
        except Exception as e:
            print(f"Error fetching from Openverse API: {e}")

    recent = user_searches.get(username, []) if username else []
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "recent": recent})
