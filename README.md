# caching-proxy-python
Flask and FastAPI based caching proxy server with TTL, clear cache and X-Cache headers

# Caching Proxy Server in Python 

This project is a simple proxy server with caching support using **Flask** and **FastAPI**.  
It forwards requests to an origin server and caches responses, adding headers to indicate cache status (`X-Cache: HIT` / `MISS`).

---

## 📁 Files

- `caching_proxy.py`: Flask-based version
- `proxy_fastapi.py`: FastAPI version

---

## 💻 Requirements

Install dependencies using:

```bash
pip install flask fastapi uvicorn requests

▶️ How to Run

Flask version: python caching_proxy.py

Visit:
http://localhost:3000/products

FastAPI version: uvicorn proxy_fastapi:app --reload --port 3000

Visit:
Swagger docs: http://localhost:3000/docs

Supported Endpoints

GET /products → fetch product data (cached)
POST /posts → add a new post (forwarded)
PUT /posts/1 → update a post (forwarded)
DELETE /posts/1 → delete a post (forwarded)
GET /clear-cache → clears the cache manually

Sample CURL Commands
GET (cached): curl http://127.0.0.1:3000/products

First time: X-Cache: MISS
Next time: X-Cache: HIT

POST: curl -X POST http://127.0.0.1:3000/posts -H "Content-Type: application/json" -d "{\"title\": \"New Post\"}"

PUT: curl -X PUT http://127.0.0.1:3000/posts/1 -H "Content-Type: application/json" -d "{\"title\": \"Updated Post\"}"

DELETE: curl -X DELETE http://127.0.0.1:3000/posts/1

Clear cache: curl http://127.0.0.1:3000/clear-cache

Auto Expiry (TTL)
The server automatically expires cache entries after 60 seconds (FastAPI version).

🚀 Project Page
https://github.com/rhakia/caching-proxy-python

Inspired by
Roadmap.sh's Caching Proxy Python project idea.
https://roadmap.sh/projects/caching-server
