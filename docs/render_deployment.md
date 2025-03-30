# JedgeBot: Render Deployment Guide

This guide walks you through deploying the JedgeBot webapp on [Render.com](https://render.com). It assumes a split deployment with FastAPI on the backend and Vite + React on the frontend.

---

## 🌐 Backend Deployment (FastAPI)

### 📁 Folder: `/backend`

### ✅ Prerequisites:
- PostgreSQL instance ready (Render or external)
- `poetry.lock` and `pyproject.toml` configured
- FastAPI app lives in `main.py`

### 🛠️ Setup Steps:

1. **Add a Start Script** (choose one)
   - In `pyproject.toml`:
     ```toml
     [tool.poetry.scripts]
     start = "uvicorn backend.main:app --host 0.0.0.0 --port 10000"
     ```
   - OR create a `Procfile`:
     ```bash
     web: uvicorn backend.main:app --host 0.0.0.0 --port 10000
     ```

2. **Install Gunicorn + Uvicorn**
   ```bash
   poetry add gunicorn uvicorn[standard]
   ```

3. **Enable CORS in FastAPI**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend-url.onrender.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Secure Cookies in Production**
   ```python
   secure = os.getenv("ENV") == "production"
   response.set_cookie(..., secure=secure, samesite="Strict", ...)
   ```

5. **Configure Environment Variables in Render**
   - `SECRET_KEY=super-secret`
   - `DATABASE_URL=your-postgres-url`
   - `ENV=production`

6. **Render Web Service Setup**
   - Type: **Web Service**
   - Root Directory: `backend/`
   - Build Command: `poetry install`
   - Start Command: `gunicorn backend.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000`

---

## 💻 Frontend Deployment (React + Vite)

### 📁 Folder: `/frontend`

### ✅ Prerequisites:
- All API requests use `VITE_API_URL`
- Vite is configured for static output

### 🛠️ Setup Steps:

1. **Build the App Locally**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Use `VITE_API_URL` in API Client**
   ```ts
   const apiUrl = import.meta.env.VITE_API_URL;
   ```

3. **Create `.env.production`**
   ```env
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

4. **Configure `vite.config.js`** (if using React Router)
   ```js
   export default defineConfig({
     plugins: [react()],
     build: {
       outDir: 'dist',
     },
     server: {
       proxy: {
         '/api': 'http://localhost:10000',
       },
     },
   });
   ```

5. **Render Static Site Setup**
   - Type: **Static Site**
   - Root Directory: `frontend/`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Environment Variables:
     - `VITE_API_URL=https://your-backend-url.onrender.com`

---

## 📬 Optional Add-ons

### 🔁 Email Support
- Use MailHog locally
- For prod, configure SMTP or SendGrid credentials in backend `.env`

### 🧪 Health Check
- Add `/health` route to backend:
   ```python
   @app.get("/health")
   def health():
       return {"status": "ok"}
   ```

### ⚙️ Database Migrations
- Run Alembic migrations manually:
   ```bash
   poetry run alembic upgrade head
   ```

---

## 🚀 Next Steps

- [ ] Test all frontend API calls with `VITE_API_URL`
- [ ] Push code to GitHub
- [ ] Link Render to GitHub repo
- [ ] Deploy backend first, then frontend
- [ ] Confirm CORS + cookies work in production

---

Happy deploying! 🎉

