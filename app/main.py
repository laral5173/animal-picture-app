"""
Animal Picture App - Tech Challenge for Camunda TAM role.

Two REST endpoints as required:
1. POST /animals/fetch  -> fetch & save N pictures of an animal type
2. GET  /animals/{animal_type}/latest -> return the last saved picture
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from contextlib import asynccontextmanager
import os

from app.database import init_db, get_db, AnimalPicture
from app.animal_service import fetch_multiple_animal_images, UnsupportedAnimalError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Animal Picture App",
    description="Fetches and stores random pictures of cats, dogs, and bears.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------- Request/Response schemas ----------

class FetchRequest(BaseModel):
    animal_type: str = Field(..., examples=["cat"], description="cat, dog, or bear")
    count: int = Field(1, ge=1, le=10, description="Number of pictures to fetch (1-10)")


class PictureResponse(BaseModel):
    id: int
    animal_type: str
    source_url: str
    file_path: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Endpoint 1: fetch & save ----------

@app.post("/animals/fetch", response_model=list[PictureResponse])
async def fetch_animal_pictures(request: FetchRequest, db: Session = Depends(get_db)):
    """
    Fetch `count` random pictures of `animal_type` from the external API,
    save them to disk, and store a record of each in the database.
    """
    try:
        fetched = await fetch_multiple_animal_images(request.animal_type, request.count)
    except UnsupportedAnimalError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch image: {e}")

    saved_records = []
    for source_url, file_path in fetched:
        record = AnimalPicture(
            animal_type=request.animal_type.lower(),
            source_url=source_url,
            file_path=file_path,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        saved_records.append(record)

    return saved_records


# ---------- Endpoint 2: get latest ----------

@app.get("/animals/{animal_type}/latest", response_model=PictureResponse)
def get_latest_animal_picture(animal_type: str, db: Session = Depends(get_db)):
    """Return the most recently saved picture for the given animal type."""
    record = (
        db.query(AnimalPicture)
        .filter(AnimalPicture.animal_type == animal_type.lower())
        .order_by(AnimalPicture.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"No pictures found for '{animal_type}'. Fetch one first via POST /animals/fetch.",
        )
    return record


# ---------- Bonus: serve the actual image file ----------

@app.get("/animals/{animal_type}/latest/image")
def get_latest_animal_image_file(animal_type: str, db: Session = Depends(get_db)):
    """Bonus endpoint: returns the actual image file (not just metadata)."""
    record = (
        db.query(AnimalPicture)
        .filter(AnimalPicture.animal_type == animal_type.lower())
        .order_by(AnimalPicture.created_at.desc())
        .first()
    )
    if not record or not os.path.exists(record.file_path):
        raise HTTPException(status_code=404, detail="Image not found.")
    return FileResponse(record.file_path)


# ---------- Bonus: simple UI ----------

@app.get("/", response_class=HTMLResponse)
def simple_ui():
    """Minimal UI to request and view an animal picture - no CSS framework needed."""
    return """
    <html>
      <head><title>Animal Picture App</title></head>
      <body style="font-family: sans-serif; max-width: 500px; margin: 40px auto;">
        <h2>🐱🐶🐻 Animal Picture App</h2>
        <select id="animal">
          <option value="cat">Cat</option>
          <option value="dog">Dog</option>
          <option value="bear">Bear</option>
        </select>
        <button onclick="fetchAndShow()">Fetch new picture</button>
        <div id="result" style="margin-top: 20px;"></div>

        <script>
          async function fetchAndShow() {
            const animal = document.getElementById('animal').value;
            document.getElementById('result').innerHTML = 'Loading...';

            await fetch('/animals/fetch', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({animal_type: animal, count: 1})
            });

            const img = document.createElement('img');
            img.src = '/animals/' + animal + '/latest/image?t=' + Date.now();
            img.style.maxWidth = '100%';
            img.style.borderRadius = '8px';

            document.getElementById('result').innerHTML = '';
            document.getElementById('result').appendChild(img);
          }
        </script>
      </body>
    </html>
    """
