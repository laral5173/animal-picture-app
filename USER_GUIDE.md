# 🐱🐶🐻 Animal Picture App — User Guide

> **For**: Anyone who wants to try the app
> **Level**: No technical knowledge required

---

## 1. What is this app?

**A simple web app that shows you random pictures of cats, dogs, and bears.**

You pick an animal, click a button, and a new picture appears on your screen. That's it.

---

## 2. How to try it (the easy way)

### Step 1: Open the app in your browser

Once the app is running (someone already started it for you), open:

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

## 3. What to expect

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

## 4. If you want to try with commands (optional)

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
Invoke-RestMethod -Uri http://localhost:8000/animals/cat/latest/image -OutFile "$env:USERPROFILE\Desktop\my_cat.jpg"
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

## 5. Where are the pictures saved?

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

## 6. Useful links

| Link | What it does |
|------|-------------|
| [http://localhost:8000](http://localhost:8000) | 🌐 The main app — pick an animal and see pictures |
| [http://localhost:8000/docs](http://localhost:8000/docs) | 📖 Interactive documentation — try the API with buttons and forms |

---

## 7. Troubleshooting

| Problem | Solution |
|---------|----------|
| Page doesn't load | Make sure the app is running. Ask the person who set it up. |
| "Failed to fetch image" error | The internet connection might be down, or the animal photo website is temporarily unavailable. Try again in a few seconds. |
| "No pictures found" error | You need to click "Fetch new picture" first before trying to view a picture. |
| Picture doesn't change | Some animal websites sometimes return the same picture twice. Click "Fetch new picture" again to get a different one. |

---

## 8. Quick start checklist

- [ ] Open http://localhost:8000 in your browser
- [ ] Select an animal (Cat, Dog, or Bear)
- [ ] Click "Fetch new picture"
- [ ] Wait 1-2 seconds
- [ ] See your animal picture! 🎉

**That's it! You're using the Animal Picture App. 🐱🐶🐻**
