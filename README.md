# 🔗 Link Saver + Auto-Summary

A full-stack web app that lets users save important links and automatically get AI-generated summaries. Organize with tags, filter, reorder, and view clean summaries — all in one lightweight interface.

---

## 🌐 Live Links

- **Frontend:** [https://link-saver-frontend.onrender.com]
- **Backend API:** [https://link-saver-9awl.onrender.com/docs]

---

## 🧰 Tech Stack

### Frontend:
- React (CRA)
- Axios
- React Router DOM
- React Markdown
- Deployed on **Render**

### Backend:
- FastAPI (Python)
- MongoDB Atlas (NoSQL database)
- Langchain + Jina AI (for summaries) *(optional/bonus)*
- Deployed on **Render**

---

## 🚀 Features

- ✅ Save links with title + summary
- ✅ Auto-generate summary using AI

---

## 🛠️ Getting Started Locally

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create a `.env` file with:
MONGO_URI=your_mongo_uri
```
Run backend:
```
uvicorn app.main:app --reload
```

### Frontend (React)
```
cd frontend
npm install
```

# In `.env`, add:
REACT_APP_BACKEND_URL=https://link-saver-9awl.onrender.com
Run frontend:
```
npm start
```

## 📸 Screenshot

screenshot1:

<img width="577" height="162" alt="Image" src="https://github.com/user-attachments/assets/4436ac19-b9fe-4c86-b4a8-134912ce1bec" />

screenshot2:


<img width="584" height="188" alt="Image" src="https://github.com/user-attachments/assets/04ba1c77-4879-429e-84cd-2380855a61ff" />

screenshot3:

<img width="1010" height="533" alt="Image" src="https://github.com/user-attachments/assets/8d7cdab6-195c-41d7-92de-7eaa567fa5df" />

---

## 💡 What I'd Do Next
- Add authentication + user dashboard

- Cloudinary screenshot previews of links

- Bookmark categorization

- Export/import bookmarks

- Browser extension (save from Chrome directly)

---

## 📚 Folder Structure

link-saver/

├── backend/
← FastAPI + MongoDB (auth + API)
│   ├── app/

│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes/
│   │   └── auth.py, bookmarks.py
├── frontend/         ← React frontend (login, save, view, delete)
│   └── src/
│       └── pages, components, api/
├── README.md
