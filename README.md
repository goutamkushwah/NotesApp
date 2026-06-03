# 📝 Notes App with Python, FastAPI & Supabase

🎥 [Watch the full YouTube tutorial here]
(https://youtu.be/ryvBJU4QqVg)

This project is a simple note-taking web app built with Python, FastAPI, and Supabase

It supports  
✅ User Registration & Login with Supabase Auth  
✅ Add, List, and Delete Notes (CRUD)  
✅ Secure Session Handling  
✅ Clean UI with HTML and CSS  

---

## 🚀 Features

- Register and login with Supabase authentication  
- Create and delete notes linked to the logged-in user  
- Session-based authentication using cookies  
- Minimal and responsive UI with HTML and CSS  

---

## 📦 Full Setup & Run (All-in-One)

Copy and run all the commands below in your terminal:

```bash
# Clone the repository
git clone https://github.com/your-username/notes-app-fastapi-supabase.git
cd notes-app-fastapi-supabase

# Create a virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn supabase python-dotenv itsdangerous jinja2

# Create .env file (you can edit it with your favorite editor)
echo "SUPABASE_URL=your-supabase-url" >> .env
echo "SUPABASE_KEY=your-service-role-key" >> .env
echo "SECRET_KEY=your-secret-key" >> .env

# Run the app
python -m uvicorn main:app --reload

# Open in your browser: http://127.0.0.1:8000
