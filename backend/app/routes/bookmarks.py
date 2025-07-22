from fastapi import APIRouter, Request, HTTPException
from app.models import BookmarkCreate
from app.database import bookmarks_collection
from jose import jwt, JWTError
from dotenv import load_dotenv
from bson import ObjectId
import os, requests, re
from bs4 import BeautifulSoup

load_dotenv()
router = APIRouter()
JWT_SECRET = os.getenv("JWT_SECRET")


# -------------------- Helper: Extract Email from Token --------------------
def get_user_email_from_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["email"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -------------------- Helper: Title & Favicon Extraction --------------------
def extract_title_and_favicon(url: str):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title"
        favicon = soup.find("link", rel=re.compile("icon", re.I))
        favicon_url = favicon['href'] if favicon else "/favicon.ico"
        if favicon_url.startswith("/"):
            favicon_url = url.split("/")[0] + "//" + url.split("/")[2] + favicon_url
        return title, favicon_url
    except:
        return "No Title", ""


# -------------------- Helper: Jina Summary --------------------
from bs4 import BeautifulSoup

def get_summary(url: str):
    try:
        encoded_url = requests.utils.quote(url, safe='')
        res = requests.get(f"https://r.jina.ai/{encoded_url}", timeout=7)
        raw_text = res.text.strip()

        # Filter noisy content
        noisy_phrases = [
            "Skip to content", "Watch Live", "Home", "News", "Sport", "Business", "Innovation",
            "Culture", "Arts", "Travel", "Earth", "Audio", "Video", "Live", "More", "Top Stories",
            "Breaking", "BBC", "---", "Sign in", "Sign up"
        ]
        for phrase in noisy_phrases:
            raw_text = raw_text.replace(phrase, "")

        lines = raw_text.splitlines()
        filtered = []
        for line in lines:
            line = line.strip()
            if len(line) > 40 and not line.startswith("http") and not line.startswith("[") and "http" not in line:
                filtered.append(line)

        if filtered:
            return "\n".join(filtered[:5])
        else:
            raise ValueError("Empty after filtering")

    except:
        # Fallback to manual scraping
        try:
            response = requests.get(url, timeout=7)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 40]
            return "\n".join(text[:5]) if text else "No useful content found."
        except:
            return "Summary unavailable."



# -------------------- POST /bookmarks --------------------
@router.post("/bookmarks")
def save_bookmark(bookmark: BookmarkCreate, request: Request):
    user_email = get_user_email_from_token(request)

    title, favicon = extract_title_and_favicon(bookmark.url)
    summary = get_summary(bookmark.url)

    data = {
        "user": user_email,
        "url": bookmark.url,
        "title": title,
        "favicon": favicon,
        "summary": summary,
    }

    result = bookmarks_collection.insert_one(data)

    return {
        "id": str(result.inserted_id),
        "user": user_email,
        "url": bookmark.url,
        "title": title,
        "favicon": favicon,
        "summary": summary
    }


# -------------------- GET /bookmarks --------------------
@router.get("/bookmarks")
def get_user_bookmarks(request: Request):
    user_email = get_user_email_from_token(request)
    bookmarks = list(bookmarks_collection.find({"user": user_email}))
    for b in bookmarks:
        b["id"] = str(b["_id"])
        del b["_id"]
    return bookmarks


# -------------------- DELETE /bookmarks/{bookmark_id} --------------------
@router.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: str, request: Request):
    user_email = get_user_email_from_token(request)

    try:
        result = bookmarks_collection.delete_one({
            "_id": ObjectId(bookmark_id),
            "user": user_email
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid bookmark ID format.")

    return {"success": result.deleted_count == 1}
