# 🐱🐶🐻 Animal Picture App — User Guide

> **For**: Anyone who wants to try the app
> **Level**: No technical knowledge required

---

## 1. What is this app?

**A simple web app that shows you random pictures of cats, dogs, and bears.**

You pick an animal, click a button, and a new picture appears on your screen. That's it.

---

## 2. Before you start — what you need

The app can run in two ways. Pick the one that works for you:

### Option A: Using Docker (recommended — no Python installation needed)

1. **Install Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop/) if you don't have it
2. **Open Docker Desktop** — look for it in your Start Menu and wait until it says "Docker Desktop is running"
3. Open PowerShell and type:

```powershell
cd c:\proyectos\animal-picture-app
docker-compose up --build
```

4. Wait a minute while it downloads and builds. You'll see a lot of text — that's normal.

### Option B: Using Python directly (no Docker needed)

1. **Install Python 3.12+** from [python.org](https://www.python.org/downloads/) if you don't have it
2. Open PowerShell and type:

```powershell
cd c:\proyectos\animal-picture-app
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ⚠️ Important: Only one at a time

You can use **either** Docker **or** Python, but not both at the same time.
If you already have one running and want to switch, stop it first (see section 7).

---

## 3. How to try it (the easy way)

### Step 1: Open the app in your browser

Once the app is running (you followed the steps above), open your browser and go to:

```
http://localhost:8000
```

You will see a simple page like this:

```
┌──────────────────────────────────────┐
│  🐱🐶🐻 Animal Picture App          │
│                                      │
│  [Cat ▾]  [Fetch new picture]        │
│                                      │
│  (picture will appear here)          │
└──────────────────────────────────────┘
```

### Step 2: Pick an animal

Click the dropdown menu and choose:
- **Cat** 🐱
- **Dog** 🐶
- **Bear** 🐻

### Step 3: Get a picture

Click the **"Fetch new picture"** button.

### Step 4: See the result

A random picture of your chosen animal will appear on the page.

![Example: a cat picture appears]

---

## 4. What to expect

| What happens | Explanation |
|-------------|-------------|
| ✅ A picture appears | The app downloaded a random animal picture from the internet |
| ✅ The picture is saved | Every picture is automatically saved to the computer |
| ✅ You can try again | Click "Fetch new picture" again to get a different picture |
| ✅ Try different animals | Switch between Cat, Dog, and Bear — each has its own collection |
| ✅ It works every time | Each click gets a fresh, random picture |

### What you might notice

- Pictures are **different every time** — they come from public animal photo websites
- If you close and reopen the app, **your old pictures are still there**
- The app works **even without internet** for pictures you already downloaded

---

## 5. If you want to try with commands (optional)

> This section is for people who like using the terminal. If you just want to click buttons, skip this part.

### Using PowerShell (Windows)

Open PowerShell and type these commands one by one:

```powershell
:: Get a cat picture
Invoke-RestMethod -Uri http://localhost:8000/animals/fetch -Method POST -Body '{"animal_type":"cat","count":1}' -ContentType "application/json"

:: Get a dog picture
Invoke-RestMethod -Uri http://localhost:8000/animals/fetch -Method POST -Body '{"animal_type":"dog","count":1}' -ContentType "application/json"

:: See the last cat picture you got
Invoke-RestMethod -Uri http://localhost:8000/animals/cat/latest

:: Download the actual cat image to your computer
$desktop = [Environment]::GetFolderPath("Desktop")
Invoke-RestMethod -Uri http://localhost:8000/animals/cat/latest/image -OutFile "$desktop\my_cat.jpg"
```

### Using curl (if you have it installed)

```bash
# Get a cat picture
curl -X POST http://localhost:8000/animals/fetch -H "Content-Type: application/json" -d '{"animal_type":"cat","count":1}'

# Get a bear picture
curl -X POST http://localhost:8000/animals/fetch -H "Content-Type: application/json" -d '{"animal_type":"bear","count":1}'

# See the last bear picture
curl http://localhost:8000/animals/bear/latest

# Download the bear image
curl http://localhost:8000/animals/bear/latest/image --output bear.jpg
```

---

## 6. Where are the pictures saved?

Every picture you fetch is saved to the computer. You can find them in:

```
📁 animal-picture-app/
   └── 📁 images/
       ├── cat_a1b2c3d4.jpg
       ├── cat_e5f6g7h8.jpg
       ├── dog_9i0j1k2l.jpg
       ├── bear_m3n4o5p6.jpg
       └── ...
```

Each file name has:
- The **animal type** (cat, dog, bear)
- A **unique code** (so no two files have the same name)
- The **file extension** (.jpg or .png)

Example: `cat_a1b2c3d4.jpg` = a cat picture with unique ID `a1b2c3d4`

---

## 7. How to stop the app

> You only need to do this if you want to switch between Docker and running it directly with Python.

### If you started it with Docker

Open PowerShell and run:

```powershell
cd c:\proyectos\animal-picture-app
docker-compose down
```

This stops the container and frees up port 8000.

### If you started it directly with Python (uvicorn)

Go to the terminal where uvicorn is running and press:

```
Ctrl + C
```

### ⚠️ Important: Port already in use?

If you see an error like `Address already in use` or `port 8000 is already occupied`,
it means another instance is still running. Stop it first:

1. **If Docker is running**: run `docker-compose down` (see above)
2. **If uvicorn is running**: press `Ctrl + C` in that terminal
3. **If you're not sure**: restart your computer, or run this command to find and kill the process:

```powershell
netstat -ano | findstr :8000
```
Look for the PID (last column), then run:
```powershell
taskkill /PID <the_number> /F
```

After stopping, wait 2-3 seconds and try again.

---

## 8. Useful links

| Link | What it does |
|------|-------------|
| [http://localhost:8000](http://localhost:8000) | 🌐 The main app — pick an animal and see pictures |
| [http://localhost:8000/docs](http://localhost:8000/docs) | 📖 Interactive documentation — try the API with buttons and forms |

---

## 9. Troubleshooting

| Problem | Solution |
|---------|----------|
| Page doesn't load | Make sure the app is running. Ask the person who set it up. |
| "Failed to fetch image" error | The internet connection might be down, or the animal photo website is temporarily unavailable. Try again in a few seconds. |
| "No pictures found" error | You need to click "Fetch new picture" first before trying to view a picture. |
| Picture doesn't change | Some animal websites sometimes return the same picture twice. Click "Fetch new picture" again to get a different one. |

---

## 10. Quick start checklist

- [ ] Open http://localhost:8000 in your browser
- [ ] Select an animal (Cat, Dog, or Bear)
- [ ] Click "Fetch new picture"
- [ ] Wait 1-2 seconds
- [ ] See your animal picture! 🎉

**That's it! You're using the Animal Picture App. 🐱🐶🐻**
