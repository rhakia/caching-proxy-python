from flask import Flask, request, Response, jsonify
import requests
import argparse
import time
import os
import pickle

app = Flask(__name__)
cache = {}
CACHE_FILE = 'cache.pkl'
CACHE_TTL = 60  # default TTL in seconds

# Load existing cache from file if it exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        cache = pickle.load(f)

@app.route('/clear-cache', methods=['GET'])
def clear_cache():
    cache.clear()
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    return jsonify({"message": "Cache cleared"}), 200

def clean_expired_cache():
    now = time.time()
    expired_keys = [key for key, (_, _, timestamp) in cache.items() if now - timestamp > CACHE_TTL]
    for key in expired_keys:
        del cache[key]
    # Save cleaned cache to disk
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

def fetch_from_origin(full_url):
    origin_response = requests.get(full_url)
    return origin_response.content, origin_response.headers, origin_response.status_code

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    clean_expired_cache() 
    origin_url = app.config['ORIGIN']
    origin_full_url = f"{origin_url}/{path}"
    method = request.method
    current_time = time.time()
    cache_key = path

    if method == 'GET':
        # Check cache
        if cache_key in cache:
            data, headers, timestamp = cache[cache_key]
            if current_time - timestamp < CACHE_TTL:
                response = Response(data, status=200)
                for k, v in headers.items():
                    response.headers[k] = v
                response.headers['X-Cache'] = 'HIT'
                return response
            else:
                del cache[cache_key]

        # Fetch from origin and cache it
        data, headers, status = fetch_from_origin(origin_full_url)
        cache[cache_key] = (data, headers, current_time)
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)
        response = Response(data, status=status)
        for k, v in headers.items():
            response.headers[k] = v
        response.headers['X-Cache'] = 'MISS'
        return response

    else:
        # Forward POST/PUT/DELETE without caching
        origin_response = requests.request(
            method=method,
            url=origin_full_url,
            headers={k: v for k, v in request.headers if k != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        response = Response(origin_response.content, status=origin_response.status_code)
        for k, v in origin_response.headers.items():
            response.headers[k] = v
        response.headers['X-Cache'] = 'BYPASS'
        return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Caching Proxy Server')
    parser.add_argument('--port', type=int, default=3000)
    parser.add_argument('--origin', required=True, help='Origin server URL (e.g. http://dummyjson.com)')
    parser.add_argument('--ttl', type=int, default=60, help='Cache time-to-live in seconds')
    args = parser.parse_args()

    app.config['ORIGIN'] = args.origin
    CACHE_TTL = args.ttl

    app.run(port=args.port)
