# caching-proxy-python
Flask and FastAPI based caching proxy server with TTL, clear cache and X-Cache headers

# Caching Proxy Server in Python 

This project is a simple proxy server with caching support using **Flask** and **FastAPI**.  
It forwards requests to an origin server and caches responses, adding headers to indicate cache status (`X-Cache: HIT` / `MISS`).

---

## 📁 Files

- `caching_proxy.py`: Flask-based version
- `proxy_fastapi.py`: FastAPI version

It acts as a middle layer between the client and an origin server, caching GET responses and returning `X-Cache: HIT` or `MISS`.

---

## 🚀 Features

✅ Caching for GET requests  
✅ Auto-expiry using TTL  
✅ `X-Cache` response header  
✅ Clear Cache with `/clear-cache` endpoint  
✅ Persistent caching using `pickle`  
✅ Support for POST/PUT/DELETE passthrough (FastAPI)

---

## 🛠️ Installation

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/caching-proxy-python.git
cd caching-proxy-python
```

### 2. Create Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies 
(Separate installations)
For Flask version:
```bash
pip install flask requests
```

For FastAPI version:
```bash
pip install fastapi uvicorn httpx
```

---

## 💻 Requirements

Install dependencies using:

```bash
pip install flask fastapi uvicorn requests
```
---

## ▶️ How to Run

Flask Proxy version: 
```bash
python caching_proxy.py --origin http://dummyjson.com --port 3000 --ttl 60
```

Then open in browser:
```bash
http://localhost:3000/products
```
You’ll get:

X-Cache: MISS on first call

X-Cache: HIT on subsequent calls

X-Cache: MISS again after TTL expires

To clear cache:
```bash
http://localhost:3000/clear-cache
```

FastAPI Proxy version: 
```bash
python proxy_fastapi.py --origin http://dummyjson.com --port 3000 --ttl 60
```
Open in browser:
```bash
http://localhost:3000/products
```
FastAPI also supports:

POST/PUT/DELETE passthrough (with X-Cache: BYPASS)

Built-in docs: http://localhost:3000/docs

---

## Supported Endpoints

GET /products → fetch product data (cached)

POST /posts → add a new post (forwarded)

PUT /posts/1 → update a post (forwarded)

DELETE /posts/1 → delete a post (forwarded)

GET /clear-cache → clears the cache manually

---

## Sample CURL Commands
GET (cached): 
```bash
curl http://127.0.0.1:3000/products
```

First time: X-Cache: MISS
Next time: X-Cache: HIT

POST: 
```bash
curl -X POST http://127.0.0.1:3000/posts -H "Content-Type: application/json" -d "{\"title\": \"New Post\"}"
```

PUT: 
```bash
curl -X PUT http://127.0.0.1:3000/posts/1 -H "Content-Type: application/json" -d "{\"title\": \"Updated Post\"}"
```

DELETE: 
```bash
curl -X DELETE http://127.0.0.1:3000/posts/1
```

Clear cache: 
```bash
curl http://127.0.0.1:3000/clear-cache
```

Auto Expiry (TTL)
The server automatically expires cache entries after 60 seconds (FastAPI version).

---

## 🚀 Project Page
https://github.com/rhakia/caching-proxy-python

---

## Inspired by
Roadmap.sh's Caching Proxy Python project idea.

https://roadmap.sh/projects/caching-server
