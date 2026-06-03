import os
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer

# Load environment variables
load_dotenv()

app = FastAPI()

# Middleware (optional CORS if you add frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS/JS if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Supabase setup
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Session secret key
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
serializer = URLSafeSerializer(SECRET_KEY)


# ------------------------------
# Helper: get current user
# ------------------------------
def get_current_user(request: Request):
    cookie = request.cookies.get("session")
    if not cookie:
        return None
    try:
        data = serializer.loads(cookie)
        return data.get("user_id")
    except Exception:
        return None


# ------------------------------
# Routes
# ------------------------------
@app.get("/")
def home(request: Request, user_id: str = Depends(get_current_user)):
    # FIXED: Explicitly defined request and template context
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user_id": user_id}
    )


@app.get("/register")
def register_page(request: Request):
    # FIXED: Explicitly passed request and name
    return templates.TemplateResponse(
        request=request, 
        name="register.html"
    )


@app.post("/register")
def register(email: str = Form(...), password: str = Form(...)):
    """Register new user using Supabase Auth"""
    auth_res = supabase.auth.sign_up({"email": email, "password": password})
    if auth_res.user:
        return RedirectResponse("/login", status_code=302)
    return {"error": "Registration failed"}


@app.get("/login")
def login_page(request: Request):
    # FIXED: Explicitly passed request and name
    return templates.TemplateResponse(
        request=request, 
        name="login.html"
    )


@app.post("/login")
def login(response: Response, email: str = Form(...), password: str = Form(...)):
    """Login with Supabase Auth and set session cookie"""
    auth_res = supabase.auth.sign_in_with_password(
        {"email": email, "password": password}
    )
    if auth_res.session:
        user_id = auth_res.user.id
        # Store session in cookie
        cookie_data = serializer.dumps({"user_id": user_id})
        response = RedirectResponse("/notes", status_code=302)
        response.set_cookie(key="session", value=cookie_data, httponly=True)
        return response
    return {"error": "Login failed"}


@app.get("/logout")
def logout(response: Response):
    """Clear the session cookie"""
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("session")
    return response


@app.get("/notes")
def get_notes(request: Request, user_id: str = Depends(get_current_user)):
    """List notes for the current user"""
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    res = supabase.table("notes").select("*").eq("user_id", user_id).execute()
    
    # FIXED: Explicitly defined request, template name, and context variables
    return templates.TemplateResponse(
        request=request,
        name="notes.html",
        context={"notes": res.data, "user_id": user_id}
    )


@app.post("/notes")
def add_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    user_id: str = Depends(get_current_user),
):
    """Add a note for the logged-in user"""
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    supabase.table("notes").insert(
        {"title": title, "content": content, "user_id": user_id}
    ).execute()
    return RedirectResponse("/notes", status_code=302)


@app.post("/notes/delete")
def delete_note(note_id: str = Form(...), user_id: str = Depends(get_current_user)):
    """Delete a note (only if it belongs to the logged-in user)"""
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    supabase.table("notes").delete().eq("id", note_id).eq("user_id", user_id).execute()
    return RedirectResponse("/notes", status_code=302)